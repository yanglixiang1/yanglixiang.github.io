from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# 替换为您的API密钥和应用ID
SPARKAI_APP_ID = '13cf3cd7'  # 您的APPID
SPARKAI_API_SECRET = 'NzYxOGY0MmFmNzA1NDU0ODc4YWFjODYy'  # 您的APISecret
SPARKAI_API_KEY = '534044590d1e95d2489c12da6b29cc4e'  # 您的APIKey
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'  # 替换为实际的API地址

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')

        # 构造请求参数
        payload = {
            "header": {
                "app_id": SPARKAI_APP_ID,
                "uid": "12345"  # 可以使用用户的唯一ID
            },
            "parameter": {
                "chat": {
                    "domain": "generalv3.5",
                    "temperature": 0.5,
                    "max_tokens": 1024,
                }
            },
            "payload": {
                "message": {
                    "text": [
                        {"role": "user", "content": user_message}
                    ]
                }
            }
        }

        # 调用AI API
        headers = {
            'Authorization': f'Bearer {SPARKAI_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            SPARKAI_URL,
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            ai_response = response.json().get('payload', {}).get('choices', [{}])[0].get('text', [{}])[0].get('content', '')
            return jsonify({'response': ai_response})
        else:
            return jsonify({'response': '抱歉，服务器暂时无法处理您的请求。'}), 500

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'response': '系统错误，请稍后再试。'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 