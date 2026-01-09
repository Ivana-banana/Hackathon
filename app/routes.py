from flask import Blueprint, Flask, render_template, request, redirect, url_for
from sqlalchemy.sql.functions import current_user

from app import db
from app.models import Expense

bp = Blueprint('main', __name__)

@bp.route('/')
def hello():
    return 'Здесь будет начальная страница'

@bp.route('/author')
def author():
    return 'Страница об авторах'

@bp.route('/registration')
def registration():
    return 'Страница регистрации'

@bp.route('/login')
def login():
    return 'Страница авторизации'

#Реализация добавления/удаления расходов
#READ
@bp.route('/expense')
def expense():
    my_expense = Expense.query.filter_by(user_id=1).order_by(Expense.date.desc()).all()
    return render_template('expenses/list.html', expenses = my_expense)

#CREATE
@bp.route('/expense/add', methods=['GET', 'POST'])
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
            user_id = 1
        )
        db.session.add(new_expense)
        db.session.commit()
        return redirect(url_for('main.expense'))
    return render_template('expenses/form.html', legend = "Добавить расход")

#UPDATE
#TODO продумать безопасность
@bp.route('/expense/edit/<int:id>', methods=['GET', 'POST'])
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
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('main.expense'))
