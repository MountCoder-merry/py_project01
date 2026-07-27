import streamlit as st
import os
from datetime import datetime
from openai import OpenAI
from streamlit import sidebar, session_state
import json

#设置页面配置项
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

#保存会话信息函数
def save_session():
    if session_state.current_session:
        session_data = {
            "nick_name": st.session_state.nick_name,
            "nature": st.session_state.nature,
            "current_session": st.session_state.current_session,
            "messages": st.session_state.messages
        }

        if not os.path.exists("sessions") :
                os.mkdir("sessions")

        with open(f"sessions/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)

def load_sessions():
    session_list = []
    #遍历目录下的所有文件
    if os.path.exists("sessions"):
        file_list = os.listdir("sessions")
        for filename in file_list:
            if filename.endswith(".json"):
                session_list.append(filename[:-5])
    return session_list

#加载指定会话信息
def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            # 读取会话数据
            with open(f"sessions/{session_name}.json","r",encoding="utf_8") as f:
                session_data = json.load(f)
                st.session_state.messages = session_data["messages"]
                st.session_state.nick_name = session_data["nick_name"]
                st.session_state.nature = session_data["nature"]
                st.session_state.current_session = session_name
    except:
        st.error("加载会话失败!")

#大标题
st.title("AI智能伴侣")
# logo
st.logo("resources/logo.png")

# 预设性格列表
PRESET_NATURES = [
    "活泼开朗的东北姑娘",
    "温柔可爱的台湾姑娘",
    "害羞的日本jk少女",
    "热情大方的av老师",
    "温柔体贴的江南女子",
    "高冷傲娇的御姐",
    "可爱粘人的小奶猫",
    "知性优雅的文艺女青年",
    "直爽豪迈的川妹子",
    "神秘冷艳的暗黑系少女",
    "元气满满的运动系女孩"
]

# system_prompt = "你是一名可爱的AI助手,你的名字叫小甜甜,请以亲切、可爱语气来回答用户的问题。"
system_prompt = """
        你叫%s，现在是用户的真实伴侣，请完全代入伴侣角色。：
        规则：
            1. 每次只回1条消息
            2. 禁止任何场景或状态描述性文字
            3. 匹配用户的语言
            4. 回复简短，像微信聊天一样
            5. 有需要的话可以用❤️🌸等emoji表情
            6. 用符合伴侣性格的方式对话
            7. 回复的内容, 要充分体现伴侣的性格特征
        伴侣性格：
            - %s
        你必须严格遵守上述规则来回复用户。
    """


#初始化聊天消息
if "messages" not in st.session_state:
    st.session_state.messages = [ ]

if "nick_name" not in st.session_state:
    st.session_state.nick_name = "小甜甜"

if "nature" not in st.session_state:
    st.session_state.nature = "温柔可爱的台湾姑娘"

if "current_session" not in st.session_state:
    st.session_state.current_session = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
#展示聊天信息
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

# 创建OpenAI客户端
client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'),    base_url="https://api.deepseek.com")

with sidebar:
    # 会话信息
    st.subheader("AI控制面板")
    if st.button("新建会话", width="stretch", icon="✏️"):
        #保存会话
        save_session()
        #创建新的会话
        if st.session_state.messages:
            st.session_state.messages = [ ]
            st.session_state.current_session = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            save_session()
            st.rerun ()

    #历史会话
    st.text("历史会话")
    session_list = load_sessions()
    for session in session_list:
        # st.button(session,width="stretch",icon="📄")
        # st.button(session,icon="❌")
        col1,col2 = st.columns([4,1])
        with col1:
            #加载会话信息
            if st.button(session,width="stretch",icon="📄",key=f"load_{session}",type="primary" if session == st.session_state.current_session else "secondary"):
                load_session(session)
                st.rerun()
        with col2:
            #删除会话信息
            if st.button("",width="stretch",icon="❌",key=f"delete_{session}"):
                pass

    st.subheader("伴侣信息")
    nick_name = st.text_input("伴侣名称",placeholder="请输入名称",value= st.session_state.nick_name)
    if nick_name:
        st.session_state.nick_name = nick_name
    nature = st.text_area("伴侣性格",placeholder="请输入性格",value= st.session_state.nature)
    if nature:
        st.session_state.nature = nature
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
            {"role": "system", "content": system_prompt %(st.session_state.nick_name, st.session_state.nature)},
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

    #保存会话信息
    save_session()