import streamlit as st
import os
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

# ==================== 侧边栏：伴侣信息 ====================
with sidebar:
    st.subheader("💕 伴侣信息")

    # --- 伴侣名称 ---
    nick_name = st.text_input(
        "伴侣名称",
        placeholder="请输入名称",
        value=st.session_state.nick_name
    )
    if nick_name:
        st.session_state.nick_name = nick_name

    st.divider()

    # --- 性格选择模式 ---
    st.markdown("**伴侣性格**")

    # 单选：预设 or 自定义
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
        # 预设单选
        selected = st.selectbox(
            "选择性格",
            options=all_options,
            index=all_options.index(st.session_state.nature) if st.session_state.nature in all_options else 0
        )
        st.session_state.nature = selected

    else:
        # 自定义输入
        custom_input = st.text_area(
            "自定义性格描述",
            placeholder="例如：外表高冷但内心柔软的程序员姐姐，喜欢二次元，说话带点毒舌...",
            value=st.session_state.nature if st.session_state.nature not in PRESET_NATURES else ""
        )

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("💾 保存到列表", use_container_width=True):
                if custom_input and custom_input not in all_options:
                    st.session_state.custom_natures.append(custom_input)
                    st.session_state.nature = custom_input
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
                    st.caption(cn[:30] + "..." if len(cn) > 30 else cn)
                with c2:
                    if st.button("删除", key=f"del_{i}"):
                        st.session_state.custom_natures.pop(i)
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

    # 流式返回
    full_response = ""
    assistant_container = st.chat_message("assistant")
    response_placeholder = assistant_container.empty()

    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            response_placeholder.write(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})