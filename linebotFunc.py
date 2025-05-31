from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, VideoSendMessage,
    ImageSendMessage, TemplateSendMessage, ButtonsTemplate,
    MessageTemplateAction, URITemplateAction, QuickReply, QuickReplyButton, MessageAction, PostbackTemplateAction,
)

line_bot_api = LineBotApi('/QuUNskkkRvFAStIozl175abe0z8YAjdAmY9FreaWp9SR2qycfxwGE+JTKIp5gbOjXWZb3XJY8UjKLpOrb0gCXel4kEtFvNZZr5evUeXS+z/e/Qzwv46tYoPgELEutItqHLKZcyuv40a1wmCP25pZwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('45af1c84bbb2b4a96f69585b8f13ef52')

baseurl = 'https://68fe-118-167-251-64.ngrok-free.app/static/'  # 注意末尾加斜線

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
    
    if mtext == '運動知識':
       try:
           message = TemplateSendMessage(
               alt_text='運動知識網站推薦',
               template=ButtonsTemplate(
                   thumbnail_image_url='https://as.chdev.tw/web/article/d/6/4/dc4ae544-62a0-46f7-84aa-9d06e08670381705395214.jpg',  # 可自換為運動相關圖
                   title='了解更多運動知識 🏋️',
                   text='點擊下方按鈕前往學習運動知識：',
                   actions=[
                       URITemplateAction(
                           label='前往閱讀',
                           uri='https://www.tuk.com.tw/fitness-knowledge/'  # 可改為你指定網站
                       )
                   ]
               )
           )
           line_bot_api.reply_message(event.reply_token, message)
       except Exception as e:
           print(f"❌ 運動知識發送失敗：{e}")
           line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤，請稍後再試！'))

    if mtext == '我想聽一句鼓勵的話':
        try:
            messages = [

                TextSendMessage(text='你已經很努力了，別忘了對自己溫柔一點 🤍')
            ]
            line_bot_api.reply_message(event.reply_token, messages)
        except Exception as e:
            print("錯誤內容：", e)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))


    if '冥想引導' in mtext:
        try:
            message = TextSendMessage(
                text='請輕輕閉上眼睛，慢慢吸一口氣，感受空氣進入身體。然後，緩緩吐氣，把緊張釋放出去。在這一刻，什麼都不必做，什麼也不需要改變。你只是靜靜地呼吸，靜靜地存在。你在這裡，這就足夠了。'
            )
            line_bot_api.reply_message(event.reply_token, message)
        except Exception as e:
            print(f"冥想引導錯誤：{e}")
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))


    elif mtext == '推薦冥想影片給我':
        try:
            message = VideoSendMessage(
                original_content_url=baseurl + 'video.mp4',
                preview_image_url=baseurl + 'cover.jpg'
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

    elif mtext == '運動音樂歌單':
        buttons_template = ButtonsTemplate(
            title='運動音樂歌單',
            text='點擊下面按鈕聽音樂！',
            actions=[
                URITemplateAction(
                    label='開啟歌單',
                    uri='https://open.spotify.com/playlist/37i9dQZF1EIgSjgoYBB2M6?si=HtecA4s6SfW5CN-zM6Z8oA'
                )
            ]
        )
        template_message = TemplateSendMessage(
            alt_text='運動音樂歌單',
            template=buttons_template
        )
        line_bot_api.reply_message(event.reply_token, template_message)

    elif mtext == '每日健康提醒':
        try:
            message = ImageSendMessage(
                original_content_url="https://i.meee.com.tw/FSn477l.jpg",
                preview_image_url="https://i.meee.com.tw/FSn477l.jpg"
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

    elif mtext == '更多資訊':
        sendButton(event)

    elif mtext == '我想聽一句鼓勵的話':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='你已經很努力了，別忘了對自己溫柔一點 🤍')
        )

    elif mtext == '今日的放鬆選項':
        try:
            message = TextSendMessage(
                text='請選擇今天想要的放鬆方式 🌸',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="瑜珈", text="我想做瑜珈")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="冥想", text="我想冥想一下")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="拉伸", text="我想拉一下筋")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="練習呼吸", text="我想練習呼吸放鬆")
                        ),
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

    elif mtext == '我想做瑜珈':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='放一點瑜珈音樂，跟著伸展一下身體吧 🧘‍♀️'))

    elif mtext == '我想冥想一下':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='找個舒服的位置，閉上眼睛，跟著這段冥想影片一起慢慢放鬆 🌌'))

    elif mtext == '我想拉一下筋':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='簡單的伸展也能讓身體釋放壓力，來做幾個動作吧 ✨'))

    elif mtext == '我想練習呼吸放鬆':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='深吸一口氣，再慢慢吐出來，感覺一下自己的節奏 🌬️'))




if __name__ == '__main__':
    app.run()
