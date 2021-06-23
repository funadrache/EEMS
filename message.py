import logging, os
import sys

# デバッグレベルのログを出力します
#logging.basicConfig(level=logging.DEBUG)

# Web API クライアントを初期化します
from slack_sdk import WebClient
client = WebClient(os.environ["SLACK_BOT_TOKEN"])

# chat.postMessage API を呼び出します
response = client.chat_postMessage(
    channel=sys.argv[1],
    text=sys.argv[2],
)
