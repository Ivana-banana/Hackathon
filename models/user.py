from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    expenses = db.relationship('Expense', backref='owner', lazy=True)

    def set_password(self, password):
        """Хеширует и сохраняет пароль"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Проверяет пароль против хеша"""
        return check_password_hash(self.password, password)

    @classmethod
    def get_by_username(cls, username):
        """Возвращает пользователя по имени или None"""
        return cls.query.filter_by(username=username).first()

    @classmethod
    def username_exists(cls, username):
        """Проверяет, существует ли пользователь с таким именем."""
        return db.session.query(cls.query.filter_by(username=username).exists()).scalar()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)