import streamlit as st
import os
from datetime import datetime
from openai import OpenAI
from streamlit import sidebar

# ==================== 配置区 ====================
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

st.title("AI智能伴侣")
# st.logo("resources/logo.png")  # 如果文件不存在会报错，建议确认存在或加try

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

# ==================== Session State 初始化 ====================
def init_session():
    defaults = {
        "messages": [],
        "nick_name": "小甜甜",
        "nature": "活泼开朗的东北姑娘",
        "nature_mode": "preset",  # 'preset' | 'custom'
        "custom_natures": [],     # 用户保存的自定义性格
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session()

if "current_session" not in st.session_state:
    st.session_state.current_session = datetime.now().strftime("%Y%m%d_%H%M%S")

# ==================== 会话管理函数 ====================
def generate_session_name():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def save_session():
    if not st.session_state.current_session:
        return

    # 清理消息，确保 JSON 可序列化
    clean_messages = []
    for msg in st.session_state.messages:
        if isinstance(msg, dict) and "role" in msg and "content" in msg:
            clean_messages.append({
                "role": str(msg["role"]),
                "content": str(msg["content"])
            })

    session_data = {
        "nick_name": str(st.session_state.nick_name),
        "nature": str(st.session_state.nature),
        "current_session": str(st.session_state.current_session),
        "messages": clean_messages,
        "custom_natures": [str(c) for c in st.session_state.custom_natures]
    }

    if not os.path.exists("sessions"):
        os.mkdir("sessions")

    filepath = f"sessions/{st.session_state.current_session}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)


def load_session(session_name):
    try:
        filepath = f"sessions/{session_name}.json"
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.messages = session_data.get("messages", [])
                st.session_state.nick_name = session_data.get("nick_name", "小甜甜")
                st.session_state.nature = session_data.get("nature", "活泼开朗的东北姑娘")
                st.session_state.custom_natures = session_data.get("custom_natures", [])
                st.session_state.current_session = session_name
    except Exception as e:
        st.error(f"加载会话失败: {e}")

def load_session(session_name):
    try:
        filepath = f"sessions/{session_name}.json"
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.messages = session_data.get("messages", [])
                st.session_state.nick_name = session_data.get("nick_name", "小甜甜")
                st.session_state.nature = session_data.get("nature", "活泼开朗的东北姑娘")
                st.session_state.custom_natures = session_data.get("custom_natures", [])
                st.session_state.current_session = session_name
    except Exception as e:
        st.error(f"加载会话失败: {e}")

def delete_session(session_name):
    try:
        filepath = f"sessions/{session_name}.json"
        if os.path.exists(filepath):
            os.remove(filepath)
        if session_name == st.session_state.current_session:
            st.session_state.messages = []
            st.session_state.current_session = generate_session_name()
    except Exception as e:
        st.error(f"删除会话失败: {e}")

# ==================== 侧边栏 ====================
with sidebar:
    st.subheader("AI控制面板")

    # --- 新建会话 ---
    if st.button("新建会话", use_container_width=True, icon="✏️"):
        save_session()
        st.session_state.messages = []
        st.session_state.current_session = generate_session_name()
        save_session()
        st.rerun()

    # --- 历史会话 ---
    st.text("历史会话")
    session_list = load_sessions()
    for session in session_list:
        col1, col2 = st.columns([4, 1])
        with col1:
            is_current = session == st.session_state.current_session
            btn_type = "primary" if is_current else "secondary"
            if st.button(session, use_container_width=True, icon="📄",
                        key=f"load_{session}", type=btn_type):
                load_session(session)
                st.rerun()
        with col2:
            if st.button("❌", use_container_width=True, key=f"delete_{session}"):
                delete_session(session)
                st.rerun()

    st.divider()

    # --- 伴侣信息 ---
    st.subheader("💕 伴侣信息")

    nick_name = st.text_input(
        "伴侣名称",
        placeholder="请输入名称",
        value=st.session_state.nick_name
    )
    if nick_name:
        st.session_state.nick_name = nick_name

    st.divider()

    # --- 性格选择 ---
    st.markdown("**伴侣性格**")

    mode = st.radio(
        "选择方式",
        options=["preset", "custom"],
        format_func=lambda x: "📋 从预设选择" if x == "preset" else "✏️ 自定义输入",
        horizontal=True,
        key="nature_mode"
    )

    # 合并预设 + 用户保存的自定义选项
    all_options = PRESET_NATURES + st.session_state.custom_natures

    if mode == "preset":
        # 预设/自定义单选
        current_idx = all_options.index(st.session_state.nature) if st.session_state.nature in all_options else 0
        selected = st.selectbox(
            "选择性格",
            options=all_options,
            index=current_idx
        )
        st.session_state.nature = selected

    else:
        # 自定义输入
        default_val = st.session_state.nature if st.session_state.nature not in PRESET_NATURES else ""
        custom_input = st.text_area(
            "自定义性格描述",
            placeholder="例如：外表高冷但内心柔软的程序员姐姐，喜欢二次元，说话带点毒舌...",
            value=default_val
        )

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("💾 保存到列表", use_container_width=True):
                if custom_input and custom_input not in all_options:
                    st.session_state.custom_natures.append(custom_input)
                    st.session_state.nature = custom_input
                    save_session()
                    st.success("已保存！")
                    st.rerun()
                elif custom_input in all_options:
                    st.warning("该性格已存在")
                else:
                    st.warning("请输入内容")

        with col2:
            if st.button("✅ 应用", use_container_width=True):
                if custom_input:
                    st.session_state.nature = custom_input
                    save_session()
                    st.success("已应用！")
                    st.rerun()

    # 显示当前性格
    st.divider()
    st.markdown(f"**当前性格：** `{st.session_state.nature}`")

    # 管理已保存的自定义性格
    if st.session_state.custom_natures:
        with st.expander("🗑️ 管理已保存的性格"):
            for i, cn in enumerate(st.session_state.custom_natures):
                c1, c2 = st.columns([4, 1])
                with c1:
                    display = cn[:30] + "..." if len(cn) > 30 else cn
                    st.caption(display)
                with c2:
                    if st.button("删除", key=f"del_{i}"):
                        st.session_state.custom_natures.pop(i)
                        # 如果当前性格是被删除的，重置为第一个预设
                        if st.session_state.nature == cn:
                            st.session_state.nature = PRESET_NATURES[0]
                        save_session()
                        st.rerun()

# ==================== 主界面：聊天区 ====================
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

# 创建OpenAI客户端
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
)

# 消息输入
prompt = st.chat_input("请输入您的问题:")
if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 构建 system prompt
    final_system = system_prompt % (st.session_state.nick_name, st.session_state.nature)

    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system", "content": final_system},
            *st.session_state.messages
        ],
        stream=True,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )

    # 流式返回（过滤思考过程）
    full_response = ""
    assistant_container = st.chat_message("assistant")
    response_placeholder = assistant_container.empty()

    for chunk in response:
        delta = chunk.choices[0].delta
        # 跳过思考过程
        if hasattr(delta, 'reasoning_content') and delta.reasoning_content:
            continue
        if delta.content is not None:
            full_response += delta.content
            response_placeholder.write(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # 自动保存会话
    save_session()