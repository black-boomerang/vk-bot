import vk
from flask import Flask, request, json
from message_handler import message_handler
from settings import token, confirmation_token

app = Flask(__name__)


@app.route('/', methods=['POST'])  # обработка входящих запросов
def processing():
    data = json.loads(request.data)

    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':  # подтверждение сервера ВК
        return confirmation_token
    elif data['type'] == 'message_new':  # новое сообщение
        vk_session = vk.Session()
        api = vk.API(vk_session, v=5.0)
        text = message_handler(data)
        user_id = data['object']['user_id']
        api.messages.send(access_token=token, user_id=str(user_id), message=text)
        return 'ok'
