import csv

#方法一
# 写
with open("csv_data/01.csv", "w", encoding="utf-8") as f:
    f.write("姓名,年龄,性别,爱好\n")  # 写入表头
    f.write("小王,18,男,'football,Java'\n")  # 写入数据
    f.write("小李,18,女,Python\n")
    f.write("小张,18,男,C++\n")
    f.write("小王,20,男,Go\n")

# 读
with open("csv_data/01.csv", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())





#csv操作 方法二
with open("csv_data/02.csv", "w", encoding="utf_8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["姓名", "年龄", "性别", "爱好"])
    writer.writeheader()
    writer.writerow({"姓名": "张三", "年龄": 18, "性别": "男", "爱好": "football"})
    writer.writerow({"姓名": "王五", "年龄": 19, "性别": "女", "爱好": "basketball"})

with open("csv_data/02.csv", "r", encoding="utf_8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)