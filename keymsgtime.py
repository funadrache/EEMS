# coding:utf-8

def DateTimeStr(dt_now, separator):
    DateTimeForm = dt_now.strftime("%Y") + separator \
            + dt_now.strftime("%m") + separator + dt_now.strftime("%d") + separator \
            + dt_now.strftime("%H") + separator + dt_now.strftime("%M") + separator \
            + dt_now.strftime("%S") + separator + dt_now.strftime("%f")
    return DateTimeForm 

import readchar
import logging, os, sys
import datetime

# デバッグレベルのログを出力します
#logging.basicConfig(level=logging.DEBUG)

# Web API クライアントを初期化します
from slack_sdk import WebClient
clientLog = WebClient(os.environ["SLACK_LOG_TOKEN"])
clientUpload = WebClient(os.environ["SLACK_UPLOAD_TOKEN"])

# Open Logging file
dt_file = datetime.datetime.now()
LogFileName = DateTimeStr(dt_file, "-") + ".csv"
f = open(LogFileName, 'w')
print("Start logging, File = " + LogFileName)

# Set Bot Channels
LoggingChannel = "#bot-test"
UploadChannel = "#logupload"

# Start key waiting loop
while True:
# Read Key character and Log datetime
    c = readchar.readkey()
    dt_now = datetime.datetime.now()
    print("Key = " + str(c) + ", Date and Time = " + DateTimeStr(dt_now, ","))
    f.write(str(c) + "," + DateTimeStr(dt_now, ",") + "\n")
    f.flush()

# chat.postMessage API を呼び出します
    response = clientLog.chat_postMessage(
        channel=LoggingChannel,
        text=":bell: キー入力は" + str(c) + "です。" \
        + dt_now.strftime("日付と時刻は %Y年%m月%d日%H時%M分%S秒です。"),
    )
# Upload Log file
    if c == 's':
        response = clientUpload.files_upload(channels=UploadChannel, file=LogFileName)
        print("Logfile " + LogFileName + " uploaded.")
# Quit and Upload Log file
    if c == 'q':
        f.close()
        response = clientUpload.files_upload(channels=UploadChannel, file=LogFileName)
        print("Logfile " + LogFileName + " uploaded.")
        break
