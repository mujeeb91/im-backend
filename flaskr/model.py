from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=True)

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class ChatMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, chat_id, member_id):
        self.chat_id = chat_id
        self.member_id = member_id


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_on = db.Column(db.DateTime)

    def __init__(self, chat_id, text, created_by):
        self.chat_id = chat_id
        self.text = text
        self.created_by = created_by
        self.created_on = datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'chat_id': self.chat_id,
            'text': self.text,
            'created_by': self.created_by,
            'created_on': self.created_on.__str__(),
        }


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


def insert_seed_data():
    try:
        is_empty_database = User.query.count() == 0
        if not is_empty_database:
            return

        # Create chat
        chat = Chat(name='test chat')
        db.session.add(chat)
        db.session.commit()

        # Create users
        users = [
            User(username='andy', password='password'),
            User(username='brock', password='password'),
            User(username='chef', password='password'),
            User(username='denver', password='password'),
            User(username='earl', password='password'),
        ]

        for idx, user in enumerate(users):
            user.set_password(user.password)
            db.session.add(user)
            db.session.commit()
            if idx < 2:  # Add first 2 users as chat members and add messages
                db.session.add(ChatMember(chat_id=chat.id, member_id=user.id))
                db.session.add(Message(
                    chat_id=chat.id,
                    text=f'text by user id {user.id}',
                    created_by=user.id)
                )
                db.session.commit()
    except Exception as e:
        print(e)
