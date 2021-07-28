def dateTimeStr(dtNow, separator):
    dateTimeForm = dtNow.strftime('%Y') + separator \
        + dtNow.strftime('%m') + separator + dtNow.strftime('%d') + separator \
        + dtNow.strftime('%H') + separator + dtNow.strftime('%M') + separator \
        + dtNow.strftime('%S') + separator + dtNow.strftime('%f')
    return dateTimeForm

import logging, os
import sys
import datetime

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path

# デフォルトに使用するフォントを変更する
resource_add_path('/usr/share/fonts/truetype/takao-gothic/')
LabelBase.register(DEFAULT_FONT, 'TakaoPGothic.ttf')
#resource_add_path('/System/Library/AssetsV2/com_apple_MobileAsset_Font6/f7be88d8810a72a553ddc7ba14c15aff10ffc581.asset/AssetData/')
#LabelBase.register(DEFAULT_FONT, 'Osaka.ttf')

# Web API クライアントを初期化
from slack_sdk import WebClient
clientLog = WebClient(os.environ['SLACK_LOG_TOKEN'])
clientUpload = WebClient(os.environ['SLACK_UPLOAD_TOKEN'])

# Set Bot Channels
LoggingChannel = '#bot-test'
UploadChannel = '#logupload'

# Global変数
tmpOrg = 0
tmpOrgAndName = ''
presentMember = ['' for i in range(0)]
orgLabelText = 'あなたの所属を選択してください'

# 所属集団のリスト
orgFile = open('organization.txt', 'r')
organization = orgFile.readlines()
# Delete LF code
for index, item in enumerate(organization):
    organization[index] = organization[index].rstrip('\n')
maxOrg = index + 1
orgFile.close()

# 名前のリスト
orgAndName = [['' for i in range(5)] for j in range(4)]
# i人がセットの名簿がj個の所属集団分ということ
orgAndNameFile = open('org_and_name.txt', 'r')
tmpReadLine = orgAndNameFile.readlines()
for j in range(4):
    for i in range(5):
        orgAndName[j][i] = tmpReadLine[(j*5)+i].rstrip('\n')
orgAndNameFile.close()

print(orgAndName)

# Open Log file and Start Logging
dtFile = datetime.datetime.now()
logFileName = dateTimeStr(dtFile, '-') + '.csv'
f = open(logFileName, 'w')
print('[Start logging] File = ' + logFileName)

dtNow = datetime.datetime.now()
response = clientLog.chat_postMessage(
    channel=LoggingChannel,
    text='■■■ロギングを開始しました。' \
       + dtNow.strftime('日付と時刻は %Y年%m月%d日%H時%M分%S秒です。'),
)

class EemsApp(App):
    def build(self):

        layout=GridLayout(cols=1)
        orgLabel = Label(text = orgLabelText, font_size='20pt', size_hint_y=0.6, color=(0.9,0.9,0.9,1))
        layout.add_widget(orgLabel)
        for i in range(maxOrg):
            btn = Button(text = organization[i], font_size='28pt')
            layout.add_widget(btn)
            if i == 0:
                btn.bind(on_press = self.PersonalName)
                btn.bind(on_press = self.setTmpOrg0)
            elif i == 1:
                btn.bind(on_press = self.PersonalName)
                btn.bind(on_press = self.setTmpOrg1)
            elif i == 2:
                btn.bind(on_press = self.PersonalName)
                btn.bind(on_press = self.setTmpOrg2)
            elif i == 3:
                btn.bind(on_press = self.PersonalName)
                btn.bind(on_press = self.setTmpOrg3)
        return layout

    def setTmpOrg0(self, button):
        global tmpOrg
        tmpOrg = 0
#        print(button)
    def setTmpOrg1(self, button):
        global tmpOrg
        tmpOrg = 1
#        print(button)
    def setTmpOrg2(self, button):
        global tmpOrg
        tmpOrg = 2
#        print(button)
    def setTmpOrg3(self, button):
        global tmpOrg
        tmpOrg = 3
#        print(button)

    def PersonalName(self, button):
        
        layout = GridLayout(cols = 1, padding = 10)

        # Instantiate the modal popup and display
        popup = Popup(title ='ニックネーム選択', content = layout)
        popup.open()

        for i in range(5):
            btn = Button(text = orgAndName[tmpOrg][i], font_size='28pt')
            layout.add_widget(btn)
            if i == 0:
                btn.bind(on_press = self.EntranceOrExit)
                btn.bind(on_press = self.setTmpOrgAndName0)
                btn.bind(on_press = popup.dismiss)
            elif i == 1:
                btn.bind(on_press = self.EntranceOrExit)
                btn.bind(on_press = self.setTmpOrgAndName1)
                btn.bind(on_press = popup.dismiss)
            elif i == 2:
                btn.bind(on_press = self.EntranceOrExit)
                btn.bind(on_press = self.setTmpOrgAndName2)
                btn.bind(on_press = popup.dismiss)
            elif i == 3:
                btn.bind(on_press = self.EntranceOrExit)
                btn.bind(on_press = self.setTmpOrgAndName3)
                btn.bind(on_press = popup.dismiss)
            elif i == 4:
                btn.bind(on_press = self.EntranceOrExit)
                btn.bind(on_press = self.setTmpOrgAndName4)
                btn.bind(on_press = popup.dismiss)

        closeButton = Button(text = '戻る', font_size='28pt', size_hint_y=0.6, background_color=(0.2,0.2,0.2,1))
        layout.add_widget(closeButton) 

        # Attach close button press with popup.dismiss action
        closeButton.bind(on_press = popup.dismiss)

    def setTmpOrgAndName0(self, button):
        global tmpOrgAndName
        tmpOrgAndName = orgAndName[tmpOrg][0]

    def setTmpOrgAndName1(self, button):
        global tmpOrgAndName
        tmpOrgAndName = orgAndName[tmpOrg][1]

    def setTmpOrgAndName2(self, button):
        global tmpOrgAndName
        tmpOrgAndName = orgAndName[tmpOrg][2]

    def setTmpOrgAndName3(self, button):
        global tmpOrgAndName
        tmpOrgAndName = orgAndName[tmpOrg][3]

    def setTmpOrgAndName4(self, button):
        global tmpOrgAndName
        tmpOrgAndName = orgAndName[tmpOrg][4]

    def EntranceOrExit(self, button):
        
        layout = GridLayout(cols = 1, padding = 10)
        enterButton = Button(text = '入室', font_size='28pt')
        layout.add_widget(enterButton)
        exitButton = Button(text = '退室', font_size='28pt')
        layout.add_widget(exitButton) 
        closeButton = Button(text = '戻る', font_size='28pt', size_hint_y=0.5, background_color=(0.2,0.2,0.2,1))
        layout.add_widget(closeButton) 

        # Instantiate the modal popup and display
        popup = Popup(title = tmpOrgAndName + 'さん入室ですか退室ですか？', content = layout)
        popup.open()

        enterButton.bind(on_press = self.clickbuttonEnterRoom)
        enterButton.bind(on_press = popup.dismiss)
        exitButton.bind(on_press = self.clickbuttonExitRoom)
        exitButton.bind(on_press = popup.dismiss)

        # Attach close button press with popup.dismiss action
        closeButton.bind(on_press = popup.dismiss)

    def clickbuttonEnterRoom(self, button):
        if tmpOrgAndName in presentMember:
            return
        presentMember.append(tmpOrgAndName)
        print(presentMember)
        dtNow = datetime.datetime.now()
        response = clientLog.chat_postMessage(
              channel=LoggingChannel,
              text = organization[tmpOrg] + ' の ' + tmpOrgAndName + ' が入室した' \
                + dtNow.strftime('日付と時刻は %Y年%m月%d日%H時%M分%S秒です。'),
        )
        record_string = organization[tmpOrg] + ',' + tmpOrgAndName + ',enter,' + dateTimeStr(dtNow, ',')
        print(record_string)
        f.write(record_string + '\n')
        f.flush()

    def clickbuttonExitRoom(self, button):
        if tmpOrgAndName in presentMember:
            presentMember.remove(tmpOrgAndName)
        else:
            return
        print(presentMember)
        dtNow = datetime.datetime.now()
        response = clientLog.chat_postMessage(
              channel=LoggingChannel,
              text = organization[tmpOrg] + ' の ' + tmpOrgAndName + ' が退室した' \
                + dtNow.strftime('日付と時刻は %Y年%m月%d日%H時%M分%S秒です。'),
        )
        record_string = organization[tmpOrg] + ',' + tmpOrgAndName + ',exit,' + dateTimeStr(dtNow, ',')
        print(record_string)
        f.write(record_string + '\n')
        f.flush()

# 最後の退出者への注意喚起
        print('在室者リストの長さは' + str(len(presentMember)))
        if len(presentMember) == 0:
            self.lastExitMessage()

    def lastExitMessage(self):
        layout = GridLayout(cols = 1, padding = 10)

        popupLabel = Label(text = '最終退出チェックリスト\n・照明OFF\n・空調OFF\n・片づけ・掃除機掛け（利用した範囲でOK）\n・給湯室・トイレ清掃\n　　（不使用の場合は清掃せずにチェックしてOK）\n・ゴミ持ち帰り\n・扉施錠\n・警備システム設定', font_size='20pt')
        closeButton = Button(text = '了解', font_size='28pt', size_hint_y=0.3)

        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)    

        # Instantiate the modal popup and display
        popup = Popup(title ='注意喚起',
                    content = layout)
        popup.open()

        # Attach close button press with popup.dismiss action
        closeButton.bind(on_press = popup.dismiss)

if __name__ == '__main__':
    EemsApp().run()

# Upload Logfile when leaving application
f.close()
response = clientUpload.files_upload(channels=UploadChannel, file=logFileName)
print('[Logfile] ' + logFileName + ' uploaded.')

