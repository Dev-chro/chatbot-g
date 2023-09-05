from flask import Flask, request, jsonify
import openai
import requests
import os

app = Flask(__name__)

openai.api_key = os.environ.get('OPENAI_API_KEY') # 環境変数からAPIキーを取得

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    message = data['message']['text']  # Google Chatからのメッセージを取得

    # ChatGPTに質問する
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "system",
                "content": "あなたはIT業界に精通している親切なアシスタントです。質問に対して日本語で返答をお願いします。"
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )
    reply = response.choices[0].message['content'].strip()

    # Google Chatに返信する
    webhook_url = os.environ.get('GOOGLE_CHAT_WEBHOOK_URL_MY') # 環境変数からウェブフックURLを取得
    requests.post(webhook_url, json={"text": reply})

    return '', 204

if __name__ == '__main__':
    app.run(port=5000)
