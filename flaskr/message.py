from flask import Blueprint, request, jsonify
from flask_api import status

from .model import Chat, ChatMember, db, Message, User
from .auth import token_required

message = Blueprint('message', __name__)


@message.route('/chats', methods=['GET'])
@token_required
def get_chats(current_user):
    chats = db.session.query(Chat).join(ChatMember).filter(ChatMember.member_id == current_user.id).all()
    return jsonify([chat.to_dict() for chat in chats]), status.HTTP_200_OK


@message.route('/chats/<int:chat_id>/messages', methods=['GET'])
@token_required
def get_messages(current_user, chat_id):
    messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.created_on.asc()).all()
    return jsonify([message.to_dict() for message in messages]), status.HTTP_200_OK


@message.route('/chats/<int:chat_id>/messages', methods=['POST'])
@token_required
def create_message(current_user, chat_id):
    #TODO: Handle case for creating a new chat and adding members
    text = request.json.get('text')
    message = Message(chat_id=chat_id, text=text, created_by=current_user.id)
    db.session.add(message)
    db.session.commit()

    return jsonify(message.to_dict()), status.HTTP_201_CREATED


@message.route('/chats/<int:chat_id>/members', methods=['GET'])
@token_required
def get_members(current_user, chat_id):
    members = db.session.query(User).join(ChatMember).filter(ChatMember.chat_id == chat_id).all()
    return jsonify([member.to_dict() for member in members]), status.HTTP_200_OK


@message.route('/chats/<int:chat_id>/members', methods=['POST'])
@token_required
def add_members(current_user, chat_id):
    # TODO: Make sure user creating the chat also gets added (from FE)
    member_ids = request.json.get('member_ids')
    for member_id in member_ids:
        is_already_member = ChatMember.query.filter_by(chat_id=chat_id, member_id=member_id).first()
        if not is_already_member:
            chat_member = ChatMember(chat_id=chat_id, member_id=member_id)
            db.session.add(chat_member)
    db.session.commit()

    return jsonify({'message': 'Members added to chat'}), status.HTTP_201_CREATED
