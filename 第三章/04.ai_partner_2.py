import streamlit as st
import os
from openai import OpenAI

#设置页面配置项
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)
#大标题
st.title("AI智能伴侣")
# logo
st.logo("resources/logo.png")

system_prompt = "你是一名可爱的AI助手,你的名字叫小甜甜,请以亲切、可爱语气来回答用户的问题。"


#初始化聊天消息
if "messages" not in st.session_state:
    st.session_state.messages = [ ]

#展示聊天信息
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

# 创建OpenAI客户端
client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'),    base_url="https://api.deepseek.com")

#消息输入框
prompt = st.chat_input("请输入您的问题:")
if prompt:
    st.chat_message("user").write(f"{prompt}")
    print("------->调用AI大模型,提示词:", prompt)
    #保护用户输入的提示词
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system", "content": system_prompt},
            *st.session_state.messages
            
        ],
        stream=True,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )

    # 非流式返回
    # print("<-----------------大模型返回的结果:", response.choices[0].message.content)
    # st.chat_message("assistant").write(response.choices[0].message.content)
    # st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})

    #流式返回
    response_message = st.empty ()
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            response_message.chat_message("assistant").write(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})