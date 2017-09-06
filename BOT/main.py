#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json
import requests
from flask import Flask, request
app = Flask(__name__)
env = os.environ

@app.route('/', methods=['GET'])
def helloPage():
        return "Hello python bot."

@app.route('/messages', methods=['POST'])
def messages():
        if is_request_valid(request):
            body = request.get_json(silent=True)
            companyId = body['companyId']
            msgObj = body['message']
            groupId = msgObj['groupId']
            messageText = msgObj['text']
            userName = msgObj['createdUserName']
            send_message(companyId, groupId, userName + 'さん、' + messageText + 'ありがとう！あなたが抱えている課題は以前、この人も抱えていたみたいだから聞いてみると解決するかもしれないよ。')
            print(body)
            return "OK"
        else:
            return "Request is not valid."


# Check if token is valid.
def is_request_valid(request):
    validationToken = env['CHIWAWA_VALIDATION_TOKEN']
    requestToken = request.headers['X-Chiwawa-Webhook-Token']
    return validationToken == requestToken

# Send message to Chiwawa server
def send_message(companyId, groupId, message):
    url = 'https://{0}.chiwawa.one/api/public/v1/groups/{1}/messages'.format(companyId, groupId)
    headers = {
        'Content-Type': 'application/json',
        'X-Chiwawa-API-Token': env['CHIWAWA_API_TOKEN']
    }
    content = {
        'text' : message,
        'attachments': [
            {
                'attachmentId': 'slct1',
                'viewType': 'text',
                'title': 'yasuhisa',
                'text': "メッセージがはいります。"
        },{
                'attachmentId': 'slct2',
                'viewType': 'text',
                'title': 'Mana',
                'text': "メッセージがはいります。"
        }],
    }
    print(json.dumps(content))
    requests.post(url, headers=headers, data=json.dumps(content))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
