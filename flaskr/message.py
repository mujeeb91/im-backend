from flask import Blueprint, request, Response, jsonify
from flask_api import status
import json

from .model import Chat, ChatMember, db, Message
from .auth import token_required

message = Blueprint('message', __name__)


@message.route('/chats', methods=['GET'])
@token_required
def get_chats():
    user_id = request.form.get('user_id')
    if not user_id:
        user_id = 1  # For testing. TODO: Replace with actual user_id
    my_chats = db.session.query(Chat).join(ChatMember).filter(ChatMember.member_id == user_id).all()
    return Response(
        response=json.dumps([chat.to_dict() for chat in my_chats]),
        status=status.HTTP_200_OK,
        mimetype='application/json'
    )


@message.route('/messages', methods=['GET'])
@token_required
def get_messages():
    chat_id = request.form.get('chat_id')
    if not chat_id:
        chat_id = 1  # For testing. TODO: Replace with actual chat_id
    messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.created_on.asc()).all()
    return Response(
        response=json.dumps([message.to_dict() for message in messages]),
        status=status.HTTP_200_OK,
        mimetype='application/json'
    )


@message.route('/messages', methods=['POST'])
@token_required
def create_message():
    #TODO: Handle case for creating a new chat and adding members
    user_id = request.json.get('user_id')
    chat_id = request.json.get('chat_id')
    text = request.json.get('text')
    if not chat_id or user_id:
        user_id = 1  # For testing. TODO: Replace with actual user_id
        chat_id = 1  # For testing. TODO: Replace with actual chat_id
    message = Message(chat_id=chat_id, text=text, created_by=user_id)
    db.session.add(message)
    db.session.commit()

    return Response(
        response=json.dumps(message.to_dict()),
        status=status.HTTP_201_CREATED,
        mimetype='application/json'
    )
