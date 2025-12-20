from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Здесь будет начальная страница'

@app.route('/author')
def author():
    return 'Страница об авторах'

@app.route('/registration')
def registration():
    return 'Страница регистрации'

@app.route('/login')
def login():
    return 'Страница авторизации'

@app.route('/user')
def user():
    return 'Страница конкретного пользователя'

@app.route('/user')
def user():
    return 'Страница конкретного пользователя'

@app.route('/expenses')
def expenses():
    return 'Расходы конкретного пользователя'

if __name__ == '__main__':
    app.run(debug=True)