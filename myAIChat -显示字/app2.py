from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# 定义 headers
headers = {
    'accept': 'application/json',
    'Authorization': 'application-666786f48b334cd1086300c2497cca18'  # API Key
}

# 获取 profile id
def get_profile_id():
    profile_url = 'http://localhost:8080/api/application/profile'  # 自己的 URL
    response = requests.get(profile_url, headers=headers)
    if response.status_code == 200:
        return response.json()['data']['id']
    else:
        print("获取 profile id 失败")
        return None

# 获取 chat id
def get_chat_id(profile_id):
    chat_open_url = f'http://localhost:8080/api/application/{profile_id}/chat/open'  # 改为自己的 URL
    response = requests.get(chat_open_url, headers=headers)
    if response.status_code == 200:
        return response.json()['data']
    else:
        print("获取 chat id 失败")
        return None

# 发送聊天消息
def send_chat_message(chat_id, payload):
    chat_message_url = f'http://localhost:8080/api/application/chat_message/{chat_id}'
    response = requests.post(chat_message_url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"发送消息失败，状态码: {response.status_code}")
        return None

# 主函数，处理消息
def get_chat_response(message, re_chat=False, stream=False):
    profile_id = get_profile_id()
    if profile_id:
        chat_id = get_chat_id(profile_id)
        if chat_id:
            chat_message_payload = {
                "message": message,
                "re_chat": re_chat,
                "stream": stream
            }
            response = send_chat_message(chat_id, chat_message_payload)
            if response:
                content = response['data']['content']
                return content
    return "Error: Unable to get a response from the API."

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_message = request.form["user_message"]
        response = get_chat_response(user_message)  # 获取聊天响应
        return jsonify({"response": response})  # 返回响应给前端

    return render_template("index2.html")  # 渲染主页

if __name__ == "__main__":
    app.run(debug=True)