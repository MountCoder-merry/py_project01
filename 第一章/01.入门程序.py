# #输出python入门语句
# # 注释快捷键(ctrl + /)
# print("hello world")
# print("hello python")

# # 占位符的使用
# name = "张三"
# age = 18
# hobby = "python"
#
# print("姓名%s 年龄%s岁 爱好%s"%(name , age , hobby))
# print(f"姓名{name} 年龄{age} 爱好{hobby}")

# # 数据输入
# name = input("请输入你的名字:")
# print(f"姓名是: {name}")

# password = input("请输入你的密码:")
# money = input("请输入你的取款金额:")
# total = 10000
# print(f"余额是{total - int(money)}")

# #match case
# day = input("请输入星期(1-7):")
# match day:
#     case "1":
#         print("今天是周一")
#     case "2":
#         print("今天是周二")
#     case "3":
#         print("今天是周三")
#     case "4":
#         print("今天是周四")
#     case "5" :
#         print("今天是周五")
#     case "6" | "7":
#         print("周末休息")
#     case "8" if day == 8:
#         print("case后面可以加if")
#     case _:
#         print("输入的星期有误")

# #100-500所有三的倍数的和
# total = 0
# i = 0
# for i in range(99 , 501 ,3):
#     total += i
# else:
#     print(f"和为:{total - 99}")
#

# #九九乘法表
# for i in range (1,10):
#     for j in range (1,i+1):
#         print(f"{j} × {i} = {i * j}", end = "\t")
#     print()


# while True:
#     user = input("请输入用户名:")
#     password = input("请输入密码:")
#
#     if(user == "" or password == ""):
#         print("用户名和密码不能为空!")
#     elif (user == "admin" and password == "666888"
#             or user == "zhangsan" and password == "123456"
#             or user == "taoge" and password == "888666"):
#         print("登录成功,进入B站首页~")
#         break
#     else:
#         print("用户名或者密码错误,请重新输入!")


#生成随机数
# import random
#
# for i in range(1000):
#     random_num = random.randint(1,100);
#     print(random_num)


# #数据容器 (列表)
# s = [11,22,33,44,66,77]
#
# print(s)
# print(s[1])
#
# s[2] = 55
# print(s)
#
# del(s[2])
# print(s)
#
# for i in s:
#     print(i)

# s = []
#
# for i in range(10):
#     num = int(input("请输入本次数字:"))
#     s.append(num)
#
# print("数字列表:",s)
#
# s.sort()
# print(s[0])
# print(s[-1])
# print(sum(s)/len(s))


# #解包
# num1 = [1,2,3]
# num2 = [4,5,6]
#
# new_list = [*num1,*num2]
# print(new_list)
#
# new_list2 = num1 + num2
# print(new_list2)


# #列表推导式
# num_list = [i**2 for i in range(1,21)]
# print(num_list)
#
#
# num1 = [22,33,44,55,11,232,445]
# new_list = [i**2 for i in num1 if i % 2 == 0]
# print(new_list)


# s = "python"
#
# print(s[0::1])
# print(s[-1::-1])

# #解包 组包
# t = (11,22,33,44)
# a,b,c,d = t
# x,*y,z = t
# print(x)
# print(*y)
# print(z)

# #使用解包和组包对ab数值进行交换
# a = 11
# b = 22
# # t = a,b
# # b,a = t
# a,b = b,a
# print(a)
# print(b)

#{avg:.1f}保留一位小数

# # 选修足球学生名单
# football_set = {"王林", "曾牛", "徐立国", "遁天", "天运子", "韩立", "厉飞雨", "乌丑", "紫灵"}
# # 选修篮球学生名单
# basketball_set = {"张铁", "墨居仁","王林", "姜老道", "曾牛", "王蝉", "韩立", "天运子", "李化元", "厉飞雨", "云露"}
# # 选修法语学生名单
# french_set = {"许木", "王卓", "十三", "虎咆", "姜老道", "天运子",  "红蝶", "厉飞雨", "韩立", "曾牛"}
# # 选修艺术学生名单
# art_set = { "遁天", "天运子", "韩立", "虎咆", "姜老道", "紫灵"}
#
# s1 = football_set.intersection(art_set)
# print(s1)
#
# s2 = football_set.intersection(basketball_set.intersection(french_set.intersection(art_set)))
# print(s2)
#
# s3 = football_set.difference(basketball_set)
# print(s3)
#
# all_set = football_set | basketball_set | french_set | art_set
# all_list = [*football_set, *basketball_set, *french_set, *art_set]
#
# for s in all_set:
#     print(f"{s} 选修了 {all_list.count(s)} 门课程")


#字典


#函数
def out_line():
    """
    
    :return:
    """
    print("hello 函数")

out_line()

