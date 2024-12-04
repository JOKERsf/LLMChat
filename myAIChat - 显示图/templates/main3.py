import gradio as gr
import random
import os
import re

# 假设图片存储在某个文件夹下，且每张图片的命名与专利号相关
IMAGE_FOLDER = "C:\\Users\\ASUS\\Desktop\\处理用代码\\打标图片"  # 替换为你本地图片存放路径

# 获取图片文件夹中的所有图片文件
def get_image_by_patent_number(patent_number):
    images = [os.path.join(IMAGE_FOLDER, f) for f in os.listdir(IMAGE_FOLDER) if f.endswith(('png', 'jpg', 'jpeg', 'gif'))]
    for image in images:
        # 假设图片文件名包含专利号
        if patent_number in image:
            return image
    return None  # 如果没有找到对应的图片，返回 None

# 检查回复中是否包含多个专利号（假设专利号以 CN 开头）
def contains_patent_number(response):
    patent_number_pattern = r"CN\d{8,12}[A-Z]?"  # 匹配专利号格式，如 CN12345678B
    return re.findall(patent_number_pattern, response)  # 返回所有匹配的专利号

# 定义对话函数
def chatbot(messages, user_input):
    # 机器人回复与用户输入相同
    bot_response = user_input
    
    # 检查回复中是否包含多个专利号
    patent_numbers = contains_patent_number(bot_response)
    
    # 去重处理
    unique_patent_numbers = list(set(patent_numbers))
    
    # 存储返回的图片路径
    image_paths = []
    
    for patent_number in unique_patent_numbers:
        image_path = get_image_by_patent_number(patent_number)
        if image_path:
            bot_response += f"（这里是关于专利号 {patent_number} 的图片）"
            image_paths.append(image_path)  # 将图片路径添加到返回的列表中
        else:
            bot_response += f"（未找到关于专利号 {patent_number} 的图片）"
    
    # 更新对话历史
    messages.append(("用户: " + user_input, "机器人: " + bot_response))
    
    # 如果有图片，返回图片列表；如果没有图片，则返回 None
    return messages, image_paths if image_paths else None

# 定义清除对话历史的函数
def clear_history():
    return []

# 创建 Gradio 界面
with gr.Blocks() as demo:
    # 创建对话框显示历史聊天信息
    chatbot_box = gr.Chatbot()
    
    # 创建输入框和提交按钮
    with gr.Row():
        user_input = gr.Textbox(placeholder="输入你的消息...", show_label=False)
        submit_btn = gr.Button("提交")
    
    # 创建清除按钮
    clear_btn = gr.Button("清除")
    
    # 设置按钮的行为
    submit_btn.click(chatbot, inputs=[chatbot_box, user_input], outputs=[chatbot_box, gr.Gallery()])
    clear_btn.click(clear_history, outputs=chatbot_box)  # 清除历史聊天信息

demo.launch()
