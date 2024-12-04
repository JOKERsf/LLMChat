import requests

# 定义headers
headers = {
    'accept': 'application/json',
    'AUTHORIZATION': 'application-666786f48b334cd1086300c2497cca18'  # api key
}


# 获取 profile id
def get_profile_id():
    profile_url = 'http://localhost:8080/api/application/profile'  # 自己的url
    response = requests.get(profile_url, headers=headers)
    if response.status_code == 200:
        return response.json()['data']['id']
    else:
        print("获取profile id失败")
        return None


# 获取 chat id
def get_chat_id(profile_id):
    chat_open_url = f'http://localhost:8080/api/application/{profile_id}/chat/open'  # 改为自己的url
    response = requests.get(chat_open_url, headers=headers)
    if response.status_code == 200:
        return response.json()['data']
    else:
        print("获取chat id失败")
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


# 主函数
def main(message, re_chat=False, stream=False):
    profile_id = get_profile_id()
    if profile_id:
        print("获取profile id成功")
        print(profile_id)
        chat_id = get_chat_id(profile_id)
        if chat_id:
            print("获取chat id成功")
            print(chat_id)
            chat_message_payload = {
                "message": message,
                "re_chat": re_chat,
                "stream": stream
            }
            response = send_chat_message(chat_id, chat_message_payload)
            if response:
                print("消息发送成功")

                # 获取reponse中的content
                content = response['data']['content']

                return content

        else:
            print("获取chat id失败")
            return None
    else:
        print("获取profile id失败")
        return None


if __name__ == "__main__":
    # 在此自定义消息内容和参数
    message = "花洒的盖板有哪些功能？分点详细回答我，并在每个点的后面加上多个相关专利号，而不止一个"
    r = main(message, re_chat=False, stream=False)