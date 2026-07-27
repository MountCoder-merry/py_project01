#定义类
class Car:
    pass

# # 创建对象
# c1 = Car()
# c1.color = "red"
# c1.brand = "BMW"
# c1.name = "X5"
# c1.price = 50000
#
# print(c1.brand)
# print(c1.__dict__)

class Car:
    def __init__(self,c_brand,c_name,c_price):
        self.brand = c_brand 
        self.name = c_name
        self.price = c_price

c1 = Car("BWM","X5",5000)
print(c1)
print(c1.__dict__)