# def rectangle_area(l,w):
#     """
#     :param l: 长方形长度
#     :param w: 长方形宽度
#     :return: 长方形的面积
#     """
#     area = l * w
#     return area
#
# help(rectangle_area)#展示说明文档,也可光标停留在指定函数上
# print(rectangle_area(20,10))

# #函数 不定长参数
# def calc_data(*args,**kwargs):
#     """
#
#     :param args: 不定长位置参数
#     :param kwargs: 不定长关键参数
#     round: 保留小数
#     :return:
#     """
#     min_data = min(args)
#     max_data = max(args)
#     avg_data = sum(args) / len(args)
#
#     if kwargs.get("round") is not None:
#         avg_data = round( avg_data , kwargs.get("round"))
#
#     if kwargs.get("print") is not None:
#         print(f"计算出来的最小值:{min_data}, 最大值:{max_data}, 平均值:{avg_data}")
#     return min_data,max_data, avg_data
#
# print(calc_data(1,2,4,6,2,3,5,round = 3, print = True))
# print(calc_data(1,2,4,6,2,3,5))


#匿名函数
out_line = lambda : print("--------------------")
add = lambda x,y : print(x + y)

out_line()
add(2,1)

data_list = ["王林", "曾牛", "徐立国", "遁天", "天运子", "韩立", "厉飞雨", "乌丑", "紫灵"]
print(data_list)

data_list.sort(key= lambda item : len(item), reverse= True) #匿名函数典型运用场景
print(data_list)
