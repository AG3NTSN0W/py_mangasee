from resource.utils import to_json
from flask import Blueprint, jsonify, request
from repository.notification_DB import Notifications, Notification
from service.notification import Notification as noti

bp = Blueprint('notification', __name__, url_prefix='/notification')

@bp.route('/', methods=['GET'])
def get():
    try:
        return jsonify(to_json(Notifications().get_notification()))
    except Exception as e:
        return {'message': f'{e}'}, 500

@bp.route('/', methods=['POST'])
def add():
    try:
        content = request.get_json()
        if not 'name' in content or not 'type' in content or not 'token' in content or not 'chatId' in content:
            return {'message': 'Missing fields | [ name, type, token, chatId ]'}, 400
        name = content['name']
        type = content['type']
        token = content['token']
        chatId = content['chatId']
        return jsonify(Notifications().add_notification(Notification(name, type, token, chatId)))
    except Exception as e:
        return {'message': f'{e}'}, 500

# @bp.route('/<int:manga_id>', methods=['GET'])
# def update(manga_id: int):
#     try:
#         return jsonify(Notifications().update_notification(manga_id).to_json())
#     except Exception as e:
#         return {'message': f'{e}'}, 500

@bp.route('/<string:name>', methods=['DELETE'])
def delete(name: str):
    try:
        return jsonify(Notifications().delete_notification(name))
    except Exception as e:
        return {'message': f'{e}'}, 500


@bp.route('/test', methods=['POST'])
def test():
    try:
        content = request.get_json()
        if not 'name' in content or not 'type' in content or not 'token' in content or not 'chatId' in content:
            return {'message': 'Missing fields | [ name, type, token, chatId ]'}, 400
        name = content['name']
        type = content['type']
        token = content['token']
        chatId = content['chatId']

        toSend = Notification(name, type, token, chatId)
        hasSend = noti.sendTo(toSend.to_tuple(), "Test Message")
        if (hasSend):
            return {'message': "Test notifictaion"}, 200
        return {'message': "Unable to send notifictaion"}, 500   
    except Exception as e:
        return {'message': f'{e}'}, 500
        