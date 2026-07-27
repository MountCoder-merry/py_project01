# Please install OpenAI SDK first: `pip3 install openai`
import os
from openai import OpenAI

client = OpenAI(    api_key=os.environ.get('DEEPSEEK_API_KEY'),    base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=[
        {"role": "system", "content": "你是一名可爱的AI助手,你的名字叫小甜甜,请以亲切、可爱语气来回答用户的问题"},
        {"role": "user", "content": "你是谁,你能为我做什么"},
    ],
    stream=False,
    reasoning_effort="high",
    extra_body={"thinking": {"type": "enabled"}}
)

print(response.choices[0].message.content)