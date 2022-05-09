from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from utils import message_creater
from line_bot_ai.line_message import LineMessage,LineImage

@csrf_exempt
def index(request):
    if request.method == 'POST':
        request = json.loads(request.body.decode('utf-8'))
        print(request)
        data = request['events'][0]
        message = data['message']
        if message['type'] == 'text':
            print('textです')
            reply_token = data['replyToken']
            line_message = LineMessage(message_creater.create_single_text_message(message['text']))
            line_message.reply(reply_token)
            return HttpResponse("ok")
        elif message['type'] == 'image':
            print('imageです')
            reply_token = data['replyToken']
            line_message = LineImage(message_creater.create_single_text_message(message['image']))
            line_message.reply(reply_token)
        else :
            print('textではない何かです')
            return HttpResponse("ok")
