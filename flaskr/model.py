from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


def populate_seed_data():
    is_empty_database = User.query.count() == 0
    if not is_empty_database:
        return

    users = [
        User(username='andy', password='password'),
        User(username='brock', password='password'),
        User(username='chef', password='password'),
        User(username='denver', password='password'),
        User(username='earl', password='password'),
    ]

    for user in users:
        user.set_password(user.password)
        db.session.add(user)
    db.session.commit()
