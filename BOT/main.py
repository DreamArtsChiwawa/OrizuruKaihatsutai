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
            if "/tell-me" in messageText or "/tellme" in messageText or "/tell_me" in messageText or "/tell me" in messageText:
                if "/tell me" in messageText:
                    msg = get_problem(messageText,2)
                    print(msg)
                    ans = search.search_similar_docs(msg,3)
                    sndMsgText = '1. ' + ans[0][1] + "さん" + '\n2. ' + ans[1][1] + "さん" + '\n3. ' + ans[2][1] + "さん"
                    send_message(companyId, groupId, userName + 'さん、その問題解決するかも!!\n' + sndMsgText)
                    print("/tell me")
                else:
                    msg = get_problem(messageText,1)
                    print(msg)
                    ans = search.search_similar_docs(msg,3)
                    sndMsgText = '1. ' + ans[0][1] + "さん" + '\n2. ' + ans[1][1] + "さん" + '\n3. ' + ans[2][1] + "さん"
                    send_message(companyId, groupId, userName + 'さん、その問題解決するかも!!\n' + sndMsgText)
                    print("/tell_me")
            elif "<< WEEKLY REPORT >>" in messageText or "総括" in messageText:
                ans = search.search_similar_docs(messageText,3)
                sndMsgText = '1. ' + ans[0][1] + "さん" + '\n2. ' + ans[1][1] + "さん" + '\n3. ' + ans[2][1] + "さん"
                send_message(companyId, groupId, userName + 'さん、週報を書いてくれてありがとう！あなたが抱えている課題は以前、この人も抱えていたみたいだから聞いてみると解決するかもしれないよ。\n' + sndMsgText)
                print("return wr")

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
    body = request.get_json(silent=True)
    msgObj = body['message']
    messageText = msgObj['text']
    ans = search.search_similar_docs(messageText,3)
    url = 'https://{0}.chiwawa.one/api/public/v1/groups/{1}/messages'.format(companyId, groupId)

    wr = []
    for i in range(len(ans)):
        wr_path = ans[i][0]
        wr.append(read_wr(wr_path))

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
                 'title': ans[0][1] + "さん",
                 'text': wr[0]
        },{
                 'attachmentId': 'slct2',
                 'viewType': 'text',
                 'title': ans[1][1] + "さん",
                 'text':  wr[1]
         },{                 'attachmentId': 'slct3',
                 'viewType': 'text',
                 'title': ans[2][1] + "さん",
                 'text':  wr[2]
         }],
    }
    requests.post(url, headers=headers, data=json.dumps(content))

def send_message2(companyId, groupId, message):
    body = request.get_json(silent=True)
    msgObj = body['message']
    messageText = msgObj['text']
    msg = get_problem(messageText,2)
    ans = search.search_similar_docs(msg,3)
    url = 'https://{0}.chiwawa.one/api/public/v1/groups/{1}/messages'.format(companyId, groupId)

    wr = []
    for i in range(len(ans)):
        wr_path = ans[i][0]
        wr.append(read_wr(wr_path))

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
                 'title': ans[0][1] + "さん",
                 'text': wr[0]
        },{
                 'attachmentId': 'slct2',
                 'viewType': 'text',
                 'title': ans[1][1] + "さん",
                 'text':  wr[1]
         },{
                 'attachmentId': 'slct3',
                 'viewType': 'text',
                 'title': ans[2][1] + "さん",
                 'text':  wr[2]
         }],
    }
    requests.post(url, headers=headers, data=json.dumps(content))

def read_wr(path):
    wr_text = ""
    with open(path) as f:
        wr_text += f.read()
    return wr_text

def get_problem(text,num):
    problem = ""
    text = text.replace("　"," ")
    text = text.split()
    text = text[num:]
    for i in text:
        problem += i
    return problem

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
