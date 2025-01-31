import re
import os
import requests
from flask import Flask, render_template, request, jsonify

# 配置 Flask 使用 'images' 文件夹作为静态文件目录
app = Flask(__name__, static_folder='images')

# 定义两个不同的 headers
original_headers = {
    'accept': 'application/json',
    'Authorization': 'application-400564c87021f9662f6f9c2538038597'  # 原本模型的 API Key
}

new_model_headers = {
    'accept': 'application/json',
    'Authorization': 'application-07588dc5c9467254d8ac69dd8c3d81cf'  # 新模型的 API Key
}

# 用于存储上一次 API 响应的内容
last_api_response = {"content": ""}

# 获取 profile id
def get_profile_id(headers):
    profile_url = 'http://localhost:8080/api/application/profile'
    response = requests.get(profile_url, headers=headers)
    if response.status_code == 200:
        return response.json()['data']['id']
    else:
        print("获取 profile id 失败")
        return None

# 获取 chat id
def get_chat_id(profile_id, headers):
    chat_open_url = f'http://localhost:8080/api/application/{profile_id}/chat/open'
    response = requests.get(chat_open_url, headers=headers)
    if response.status_code == 200:
        return response.json()['data']
    else:
        print("获取 chat id 失败")
        return None

# 发送聊天消息
def send_chat_message(chat_id, payload, headers):
    chat_message_url = f'http://localhost:8080/api/application/chat_message/{chat_id}'
    response = requests.post(chat_message_url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"发送消息失败，状态码: {response.status_code}")
        return None

# 主函数，处理消息
def get_chat_response(message, re_chat=False, stream=False):
    """
    主函数，根据用户输入内容判断调用哪个模型的 API。
    """
    global last_api_response

    # 检测 "给出相关专利附图"
    if message.strip() == "给出相关专利附图":
        patent_numbers = extract_all_patent_numbers(last_api_response["content"])
        if patent_numbers:
            html_output = ""
            for patent in patent_numbers:
                html_output += f"<p>专利 {patent} 的附图是：</p>"
                html_output += f"<img src='/images/{patent}.png' alt='专利 {patent} 的附图' style='height:auto; width:500px;' /><br>"
            return html_output
        else:
            return "未找到相关专利号，请先查询相关内容。"

    # 检测 "对专利 CNxxxxxxx 的附图进行幻化"
    if message.strip().startswith("对专利") and "的附图进行幻化" in message:
        # 提取完整专利号
        patent_number = extract_patent_number(message)
        if patent_number:
            # 获取文件夹中与专利号相关的所有图片
            image_folder = app.static_folder
            matching_images = [f for f in os.listdir(image_folder) if f.startswith(patent_number) and f.endswith(".png")]

            # 排除与专利号完全匹配的图片
            main_image = f"{patent_number}.png"
            matching_images = [img for img in matching_images if img != main_image]

            if matching_images:
                html_output = f"<p>专利 {patent_number} 附图的幻化图如下：</p>"
                for image in matching_images:
                    html_output += f"<img src='/images/{image}' alt='专利 {patent_number} 的幻化附图' style='height:auto; width:500px;' /><br>"
                return html_output
            else:
                return f"未找到专利 {patent_number} 的其他附图。"
        else:
            return "未找到专利号，请确认输入格式正确。"

    # 根据用户输入内容选择 API 模型
    headers = new_model_headers if "相关专利号" in message else original_headers
    profile_id = get_profile_id(headers)
    if profile_id:
        chat_id = get_chat_id(profile_id, headers)
        if chat_id:
            chat_message_payload = {
                "message": message,
                "re_chat": re_chat,
                "stream": stream
            }
            response = send_chat_message(chat_id, chat_message_payload, headers)
            if response:
                content = response['data']['content']
                last_api_response["content"] = content
                formatted_response = format_response(content)
                return formatted_response
    return "Error: Unable to get a response from the API."

# 提取专利号
def extract_patent_number(text):
    """
    从文本中提取单个专利号（格式：CN**********[U/Z]）。
    """
    match = re.search(r"CN\d{9,}[A-Z]?", text)
    if match:
        return match.group(0)
    return None

# 提取所有专利号
def extract_all_patent_numbers(text):
    """
    从文本中提取所有专利号（格式：CN**********[U/Z]）。
    """
    matches = re.findall(r"CN\d{9,}[A-Z]?", text)
    return matches if matches else []

# 格式化响应内容，将换行符转换为 HTML 换行
def format_response(text):
    """
    遍历文本并将换行符替换为 HTML 的 <br>。
    """
    result = text.replace("\n", "<br>")
    return result

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_message = request.form["user_message"]
        response = get_chat_response(user_message)  # 获取聊天响应
        return jsonify({"response": response})  # 返回响应给前端

    return render_template("index2.html")  # 渲染主页

if __name__ == "__main__":
    app.run(debug=True)
