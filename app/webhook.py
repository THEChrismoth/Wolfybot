import flask
import urllib.parse

from flask import Flask, request
from handlers.messages.ai.pay import get_payment

app = Flask(__name__)


@app.route('/payment', methods=['POST'])
async def payment_notification_handler():
    if request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
        name = request.stream.read().decode('utf-8')
        parse_date = urllib.parse.parse_qs(name)
        vk_id = int(parse_date.get('label', [''])[0])
        balance = float(parse_date.get('amount', [''])[0])
        await get_payment(vk_id, balance)
        return 'Successful', 200
    else:
        flask.abort(403)
