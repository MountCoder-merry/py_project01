from lxml import html

with open("resources/仙逆人物志.html","r",encoding="utf_8") as f:
    html_text = f.read()

    document = html.fromstring(html_text)

    th_list = document.xpath("//table/thead/tr/th/text()")
    print(th_list)

    # tr_list = document.xpath("//table/tbody/tr[1]/td/text()")
    # print(tr_list)
    tr_list = document.xpath("//table/tbody/tr")
    for tr in tr_list:
        td_list = tr.xpath("./td/text()")
        print(td_list)
