from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash
from sqlalchemy.sql.functions import current_user
from sqlalchemy import func
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta

from app import db
from app.models import Expense, User

bp = Blueprint('main', __name__)


@bp.route('/')
@login_required
def hello():
    now = datetime.utcnow()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=31)

    my_total = db.session.query(func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.id, Expense.date >= week_ago).scalar() or 0

    my_count = Expense.query.filter(
        Expense.user_id == current_user.id, Expense.date >= week_ago).count() or 0

    top_categories = (db.session.query(Expense.category, func.sum(Expense.amount).label('amount')).filter(
        Expense.user_id == current_user.id, Expense.date >= week_ago).group_by(Expense.category)
                      .order_by(func.sum(Expense.amount).desc())
                      .limit(3).all())

    all_users_expenses = (db.session.query(User.username, func.sum(Expense.amount).label('amount'))
                          .join(Expense, User.id == Expense.user_id)
                          .filter(Expense.date >= month_ago).group_by(User.username)
                          .order_by(func.sum(Expense.amount).desc()).all())

    return render_template('expenses/main.html',
                           user=current_user, my_total=my_total, my_count=my_count,
                           top_categories=top_categories, all_users_expenses=all_users_expenses)

@bp.route('/author')
def author():
    return render_template('expenses/author.html')

@bp.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form.get('name', '').strip()
        password = request.form.get('password', '')
        if not username or not password:
            flash("Имя и пароль обязательны!")
        elif len(username) < 3:
            flash("Имя должно содержать хотя бы 3 символа.")
        elif User.username_exists(username):
            flash("Пользователь с таким именем уже существует!")
        else:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash("Регистрация успешна! Теперь войдите.")
            return redirect(url_for('main.login'))
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = User.get_by_username(username)
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.hello'))
        else:
            flash("Неверное имя пользователя или пароль!")
    return render_template('login.html')

@bp.route('/logout')
def logout():
    logout_user()
    flash("Вы успешно вышли из аккаунта!")
    return redirect(url_for('main.login'))

#Реализация добавления/удаления расходов
#READ
@bp.route('/expense')
@login_required
def expense():
    my_expense = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()
    return render_template('expenses/list.html', expenses = my_expense)

#CREATE
@bp.route('/expense/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        category = request.form.get('category')
        amount = float(request.form.get('amount'))
        comment = request.form.get('comment')
        paytype = request.form.get('paytype')

        new_expense = Expense(
            category = category,
            amount = amount,
            comment = comment,
            paytype = paytype,
            user_id = current_user.id
        )
        db.session.add(new_expense)
        db.session.commit()
        return redirect(url_for('main.expense'))
    return render_template('expenses/form.html', legend = "Добавить расход")

#UPDATE
#TODO продумать безопасность
@bp.route('/expense/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_expense(id):
    expense = Expense.query.get_or_404(id)

    if request.method == 'POST':
        expense.amount = float(request.form.get('amount'))
        expense.comment = request.form.get('comment')
        expense.paytype = request.form.get('paytype')
        expense.category = request.form.get('category')
        db.session.commit()

        return redirect(url_for('main.expense'))
    return render_template('expenses/form.html', expense = expense, legend="Редактировать")

#DELETE
@bp.route('/expense/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('main.expense'))
