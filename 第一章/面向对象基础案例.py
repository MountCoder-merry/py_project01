class Student:
    def __init__(self,name,chinese,math,english):
        self.name = name
        self.chinese = chinese
        self.math = math
        self.english = english

    def __str__(self):
        return (f"姓名:{self.name} | 语文:{self.chinese} | 数学:{self.math} | 英语:{self.english} "
                f"| 总分:{self.chinese+self.math+self.math+self.english}")


    def update_score(self,chinese = None,math = None,english = None):
        if chinese is not None:
            self.chinese = chinese
        if math is not None:
            self.math = math
        if english is not None:
            self.english = english


if __name__ == "__main__":
    s1 = Student("王林",90,88,70)
    print(s1)

    s1.update_score(chinese = 100)
    print(s1)
