from lxml import html

with open("resources/仙逆人物志.html","r",encoding="utf-8") as f:
    html_text = f.read()

    document = html.fromstring(html_text)

    #解析表头
    th_list = document.xpath("//table/thead/tr/th/text()")
    print(th_list)
    # #解析表格中的数据
    # #获取第一行数据
    # td_list = document.xpath("//table/tbody/tr[1]/td/text()")
    # print(td_list)
    #获取所有行数据
    tr_list = document.xpath("//table/tbody/tr")
    for tr in tr_list:
        td_list = tr.xpath("./td/text()")
        print(td_list)

#2026-7-30日 github提交
#2026-7-30日 github提交2
#2026-7-30日 github提交9