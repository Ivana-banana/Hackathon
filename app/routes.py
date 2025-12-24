from flask import Blueprint, Flask

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

@bp.route('/user')
def user():
    return 'Страница конкретного пользователя'

@bp.route('/expenses')
def expenses():
    return 'Расходы конкретного пользователя'