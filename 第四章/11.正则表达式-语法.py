import re

s1 = "18809090000是我的手机号，188开头的，以00结尾的；我的另一个手机号是15500008888，两个QQ号分别是1259989092和13809091293821，邮箱为python666@163.com，请给我发邮件。"

# 正则表达式
# 量词匹配
print(re.findall(r"188.*", s1))           # * 匹配0个或多个（贪婪匹配）
print(re.findall(r"188.?", s1))           # ? 匹配0个或1个
print(re.findall(r"188.+", s1))           # + 匹配1个或多个

print(re.findall(r"188\d{8}", s1))        # {8} 匹配8个数字
print(re.findall(r"155\d{6,10}", s1))     # {6,10} 匹配6到10个数字
print(re.findall(r"155\d{6,}", s1))       # {6,} 匹配6个或更多数字

# 字符集匹配
print(re.findall(r"1[38]\d{8}", s1))       # [38] 匹配3或8
print(re.findall(r"1[^38]\d{8}", s1))      # [^38] 匹配非3或8的字符
print(re.findall(r"1[3-9]\d{8}", s1))      # [3-9] 匹配3到9的范围
print(re.findall(r"^1[3-9]\d{8}", s1))     # ^ 匹配字符串开头
print(re.findall(r"^1[3-9]\d{8}$", s1))    # $ 匹配字符串结尾

# 特殊字符类匹配
print(re.findall(r"\w+\d\w+\.\w+", s1))   # \w 匹配任何单词字符(默认包含Unicode)
print(re.findall(r"\w+\d\w+\.\w+", s1, re.ASCII))  # re.ASCII 只匹配ASCII字符

# 邮箱匹配
print(re.findall(r"\w+@\w+\.\w+", s1))    # \w 匹配任何单词字符(默认行为)
print(re.findall(r"\w+@\w+\.\w+", s1, re.ASCII))  # re.ASCII 只匹配ASCII字符

# 日期匹配
s2 = "现在的时间是2026-02-06 10:05:25，今天的天气还可以，气温是28度"
print(re.findall(r"\d{4}-\d{2}-\d{2}", s2))         # 匹配完整日期
print(re.findall(r"(\d{4})-(\d{2})-(\d{2})", s2))     # 使用括号分组捕获月份和日期