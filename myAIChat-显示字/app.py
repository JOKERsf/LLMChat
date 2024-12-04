from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# 替换为新的API请求函数
def get_chat_response(api_key, message):
    # MaxKB API Base URL
    url = "https://maxkb.fit2cloud.com/api/application/625e508c-9996-11ef-9341-0242ac110003/chat/completions"  # MaxKB 的 API URL
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",  # 使用提供的 API Key
    }

    # 构建请求数据，按照 OpenAI 的格式
    data = {
        "model": "gpt-3.5-turbo",  # 你可以选择模型名称，根据 MaxKB 支持的模型
        "messages": [
            {"role": "system", "content": "你是杭州飞致云信息科技有限公司旗下产品 MaxKB 知识库问答系统的智能小助手，你的工作是帮助 MaxKB 用户解答使用中遇到的问题，用户找你回答问题时，你要把主题放在 MaxKB 知识库问答系统身上。"},
            {"role": "user", "content": message}
        ]
    }

    # 发送 POST 请求
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # 检查 HTTP 状态码
        response_data = response.json()

        # 打印原始响应数据用于调试
        print("Response Data:", response_data)

        # 解析响应数据
        if "choices" in response_data:
            chat_response = response_data["choices"][0]["message"]["content"]
            return chat_response
        else:
            return f"Error: No choices in the response. Response Data: {response_data}"

    except requests.exceptions.RequestException as e:
        # 捕获 HTTP 请求错误
        return f"Error: Unable to get a response from the API. Exception: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_message = request.form["user_message"]
        api_key = "application-666786f48b334cd1086300c2497cca18"  # 使用提供的 API Key
        response = get_chat_response(api_key, user_message)
        print(response)
        return {"response": response}

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
