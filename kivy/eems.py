#-*- coding: utf-8 -*-

def DateTimeStr(dt_now, separator):
    DateTimeForm = dt_now.strftime("%Y") + separator \
        + dt_now.strftime("%m") + separator + dt_now.strftime("%d") + separator \
        + dt_now.strftime("%H") + separator + dt_now.strftime("%M") + separator \
        + dt_now.strftime("%S") + separator + dt_now.strftime("%f")
    return DateTimeForm

import logging, os
import sys
import datetime

from kivy.app import App
from kivy.uix.widget import Widget

from kivy.properties import StringProperty, ListProperty

from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path

# デフォルトに使用するフォントを変更する
resource_add_path('/usr/share/fonts/truetype/takao-gothic/')
LabelBase.register(DEFAULT_FONT, 'TakaoPGothic.ttf') #日本語が使用できるように日本語フォントを指定する

# Web API クライアントを初期化します
from slack_sdk import WebClient
clientLog = WebClient(os.environ["SLACK_LOG_TOKEN"])
clientUpload = WebClient(os.environ["SLACK_UPLOAD_TOKEN"])

# Set Bot Channels
LoggingChannel = "#bot-test"
UploadChannel = "#logupload"

# Open Logging file
dt_file = datetime.datetime.now()
LogFileName = DateTimeStr(dt_file, "-") + ".csv"
f = open(LogFileName, 'w')
print("[Start logging] File = " + LogFileName)

dt_now = datetime.datetime.now()
response = clientLog.chat_postMessage(
    channel=LoggingChannel,
    text="■■■ロギングを開始しました。" \
    + dt_now.strftime("日付と時刻は %Y年%m月%d日%H時%M分%S秒です。"),
)

class TextWidget(Widget):
    text  = StringProperty()
    color = ListProperty([1,1,1,1])

    def __init__(self, **kwargs):
        super(TextWidget, self).__init__(**kwargs)
        self.text = '入退室記録開始'

    def buttonClicked1(self):
        self.text = '地元です'
        self.color = [1, 0, 0 , 1]
        dt_now = datetime.datetime.now()
        response = clientLog.chat_postMessage(
                    channel=LoggingChannel,
                        text='地元が押された' \
                        + dt_now.strftime("日付と時刻は %Y年%m月%d日%H時%M分%S秒です。"),
                        )
        print("地元・地域," + DateTimeStr(dt_now, ","))
        f.write("地元・地域," + DateTimeStr(dt_now, ",") + "\n")
        f.flush()

    def buttonClicked2(self):
        self.text = 'Panasonicです'
        self.color = [0, 1, 0 , 1 ]
        dt_now = datetime.datetime.now()
        response = clientLog.chat_postMessage(
                    channel=LoggingChannel,
                        text='Panasonicが押された' \
                        + dt_now.strftime("日付と時刻は %Y年%m月%d日%H時%M分%S秒です。"),
                        )
        print("Panasonic," + DateTimeStr(dt_now, ","))
        f.write("Panasonic," + DateTimeStr(dt_now, ",") + "\n")
        f.flush()

    def buttonClicked3(self):
        self.text = '学生です'
        self.color = [0, 0, 1 , 1 ]
        dt_now = datetime.datetime.now()
        response = clientLog.chat_postMessage(
                    channel=LoggingChannel,
                        text='学生が押された' \
                        + dt_now.strftime("日付と時刻は %Y年%m月%d日%H時%M分%S秒です。"),
                        )
        print("学生," + DateTimeStr(dt_now, ","))
        f.write("学生," + DateTimeStr(dt_now, ",") + "\n")
        f.flush()

    def buttonClicked4(self):
        self.text = 'その他です'
        self.color = [1, 1, 0 , 1 ]
        dt_now = datetime.datetime.now()
        response = clientLog.chat_postMessage(
                    channel=LoggingChannel,
                        text='その他が押された' \
                        + dt_now.strftime("日付と時刻は %Y年%m月%d日%H時%M分%S秒です。"),
                        )
        print("その他," + DateTimeStr(dt_now, ","))
        f.write("その他," + DateTimeStr(dt_now, ",") + "\n")
        f.flush()

    def buttonClicked5(self):
        self.text = 'Uploading CSV'
        self.color = [1, 1, 1 , 1 ]
        # Upload Logfile when button 5 clicked, file should not be closed
        response = clientUpload.files_upload(channels=UploadChannel, file=LogFileName)
        print("[Logfile] " + LogFileName + " uploaded.")

class EemsApp(App):
    def __init__(self, **kwargs):
        super(EemsApp, self).__init__(**kwargs)
        self.title = '入退室'

if __name__ == '__main__':
    EemsApp().run()

# Upload Logfile when leaving application
f.close()
response = clientUpload.files_upload(channels=UploadChannel, file=LogFileName)
print("[Logfile] " + LogFileName + " uploaded.")
