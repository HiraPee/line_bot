from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import urllib.request
import json
import os

REPLY_ENDPOINT_URL = "https://api.line.me/v2/bot/message/reply"
base = os.path.dirname(os.path.abspath(__file__))

json_open = open(base + '/AccessToken.json', 'r')
json_load = json.load(json_open)
print(json_load)
ACCESSTOKEN = json_load['ACCESSTOKEN']
HEADER = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + ACCESSTOKEN
}


class LineMessage():
    def __init__(self, messages):
        self.messages = messages

    def reply(self, reply_token):
        body = {
            'replyToken': reply_token,
            'messages': self.messages
        }
        print(body)
        req = urllib.request.Request(REPLY_ENDPOINT_URL, json.dumps(body).encode(), HEADER)
        try:
            with urllib.request.urlopen(req) as res:
                body = res.read()
        except urllib.error.HTTPError as err:
            print(err)
        except urllib.error.URLError as err:
            print(err.reason)


class LineImage():
    def __init__(self, image):
        self.image = image

    def reply(self, reply_token):
        body = {
            'replyToken': reply_token,
            'image': self.image
        }
        print(body)

        @handler.add(MessageEvent, message=ImageMessage)
        def handle_image(event):
            print('handler')
            message_id = event.message.id
            # message_idから画像のバイナリデータを取得
            message_content = line_bot_api.get_message_content(message_id)
            with open(Path(f"static/images/{message_id}.jpg").absolute(), "wb") as f:
                 # バイナリを1024バイトずつ書き込む
                 for chunk in message_content.iter_content():
                     f.write(chunk)

            main_image_path = f"static/images/{message_id}_main.jpg"
            preview_image_path = f"static/images/{message_id}_preview.jpg"
            # 画像の送信
            image_message = ImageSendMessage(
                original_content_url=f"https://date-the-image.herokuapp.com/{main_image_path}",
                preview_image_url=f"https://date-the-image.herokuapp.com/{preview_image_path}",)

            line_bot_api.reply_message(event.reply_token, image_message)
        req = urllib.request.Request(REPLY_ENDPOINT_URL, json.dumps(body).encode(), HEADER)
        try:
            with urllib.request.urlopen(req) as res:
                body = res.read()
        except urllib.error.HTTPError as err:
            print(err)
        except urllib.error.URLError as err:
            print(err.reason)
