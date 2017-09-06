#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys,os
import json
import requests
from flask import Flask, request
app = Flask(__name__)
env = os.environ
# BASE DIRECTORY SETTING
bs = os.getcwd() + '/../AI'
sys.path.append(bs)
import search
import train

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
            ans = search.search_similar_docs(messageText,3)
            print("==========================")
            print(ans)
<<<<<<< HEAD
            sndMsgText = '1. ' + ans[0][1] + '\n2. ' + ans[1][1] +  '\n3. ' + ans[2][1]
            send_message(companyId, groupId, userName + 'さん、週報を書いてくれてありがとう！あなたが抱えている課題は以前、この人も抱えていたみたいだから聞いてみると解決するかもしれないよ。\n' + sndMsgText)
=======
            sndMsgText = '1. ' + ans[0][1] + '\n2. ' + ans[1][1] + '\n3. ' + ans[2][1]
            send_message(companyId, groupId, userName + 'さん、週報を書いてくれてありがとう！あなたが抱えている課題は以前、この人も抱えていたみたいだから聞いてみると解決するかもしれないよ。\n' + sndMsgText)
            
>>>>>>> a4ab56b07f06fb7873229c581d3113f06736a512
            return "OK"
        else:
            return "Request is not valid."



def send_ai(msg):
    if is_request_valid(request):
        body = request.get_json(silent=True)
        messageText = msgObj['text']
        # AIに送るための関数などを作り、知話輪から受信したデータをAIに送る処理と結果を受け取る処理を記述する（結果は配列で帰ってくる）

        # メッセージを作るための変数を作る

# Check if token is valid.
def is_request_valid(request):
    validationToken = env['CHIWAWA_VALIDATION_TOKEN']
    requestToken = request.headers['X-Chiwawa-Webhook-Token']
    return validationToken == requestToken

# Send message to Chiwawa server
def send_message(companyId, groupId, message):
<<<<<<< HEAD
    ans = search.search_similar_docs(messageText,3)
=======
    body = request.get_json(silent=True)
    msgObj = body['message']
    messageText = msgObj['text']
    ans = search.search_similar_docs(messageText)
>>>>>>> a4ab56b07f06fb7873229c581d3113f06736a512
    url = 'https://{0}.chiwawa.one/api/public/v1/groups/{1}/messages'.format(companyId, groupId)
    headers = {
        'Content-Type': 'application/json',
        'X-Chiwawa-API-Token': env['CHIWAWA_API_TOKEN']
    }
    content = {
        'text' : message,
        'attachments': [
<<<<<<< HEAD
            {
                'attachmentId': 'slct1',
                'viewType': 'text',
                'title': ans[0][0],
                'text': "メッセージがはいります。"
        # },{
        #         'attachmentId': 'slct2',
        #         'viewType': 'text',
        #         'title': 'Mana',
        #         'text': "メッセージがはいります。"
        }],
=======
         {
                 'attachmentId': 'slct1',
                 'viewType': 'text',
                 'title': ans[0][0],
                 'text': "メッセージがはいります。"
        },{
                 'attachmentId': 'slct2',
                 'viewType': 'text',
                 'title': ans[1][1] + "さん",
                 'text':  ans[1][1] +"さんのwrのパスは" +  ans[1][0] + "にあります。"
         }],
>>>>>>> a4ab56b07f06fb7873229c581d3113f06736a512
    }
    requests.post(url, headers=headers, data=json.dumps(content))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
