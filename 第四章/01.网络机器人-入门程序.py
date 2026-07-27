import requests

#目标网址
target_url="https://www.tiobe.com/tiobe-index/"
#
response = requests.get(target_url)

#输出相应内容
print(response.text)