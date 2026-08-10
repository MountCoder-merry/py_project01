import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
}


import  requests
import csv
from lxml import html

#常量
MOVIE_LIST_FILE = "csv_data/movie_list.csv"
TMDB_BASE_URL = "https://www.themoviedb.org"
TMDB_TOP_URL_1 = "https://www.themoviedb.org/movie/top-rated"
TMDB_TOP_URL_2= "https://www.themoviedb.org/discover/movie/items"

def save_all_movies(all_movies):
    with open(MOVIE_LIST_FILE, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["电影名", "年份", "上映时间", "类型", "时长", "评分", "语言", "导演", "作者", "宣传语", "简介"])
        writer.writeheader()  # 写入表头
        writer.writerows(all_movies)  # 写入数据


def get_movie_info(movie_info_url):
    movie_response = requests.get(movie_info_url, timeout=60)

    # 解析数据，获取电影详情
    movie_doc = html.fromstring(movie_response.text)

    movie_names = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/h2/a/text()")  # 电影名称
    movie_years = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/h2/span/text()")  # 上映年份
    movie_dates = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[2]/text()")  # 上映时间
    movie_tags = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[3]/a/text()")  # 类型
    movie_cost_times = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/div/span[4]/text()")  # 时长

    # movie_scores = movie_doc.xpath("//*[@id='consensus_pill']/div[1]/div/div/@data-percent")  # 评分
    movie_scores = movie_doc.xpath("//*[@id='consensus_pill']/div/div[1]/div/div/@data-percent")  # 评分
    # movie_languages = movie_doc.xpath("//*[@id='media_v4']/div/div[2]/div/section/div[1]/div/section[1]/p[3]/text()")  # 语言
    movie_languages = movie_doc.xpath("//*[@id='media_v4']/div/div/div[2]/div/section/div[1]/div/section[1]/p[3]/text()")  # 语言
    movie_directors = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/ol/li[1]/p[1]/a/text()")  # 导演
    movie_authors = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/ol/li[2]/p[1]/a/text()")  # 作者
    movie_slogans = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/h3[1]/text()")  # 宣传语
    movie_descriptions = movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[3]/div/p/text()")  # 简介
    #
    # 3. 返回电影详情 - 字典

    movie_info = {
        "电影名": movie_names[0].strip() if movie_names else '',
        "年份": movie_years[0].strip() if movie_years else '',
        "上映时间": movie_dates[0].strip() if movie_dates else '',
        "类型": ", ".join(movie_tags) if movie_tags else '',
        "时长": movie_cost_times[0].strip() if movie_cost_times else '',
        "评分": movie_scores[0].strip() if movie_scores else '',
        "语言": movie_languages[0].strip() if movie_languages else '',
        "导演": ", ".join(movie_directors) if movie_directors else '',
        "作者": ", ".join(movie_authors) if movie_authors else '',
        "宣传语": movie_slogans[0].strip() if movie_slogans else '',
        "简介": movie_descriptions[0].strip() if movie_descriptions else ''
    }

    print(movie_info)

    return movie_info
def main():
    all_movies = []
    for page_num in range(1, 6):
        # 1. 发送请求
        if page_num == 1:
            response = requests.get(TMDB_TOP_URL_1, headers=HEADERS, timeout=60)
        else:
            data = {
                "page": page_num,
                "sort_by": "vote_average.desc",
                "vote_count.gte": 300,
                "release_date.lte": "2027-02-10",
                "show_me": "everything",
                "include_adult": "false",
                "watch_region": "HK",
                "certification_country": "HK",
            }
            response = requests.post(TMDB_TOP_URL_2, data=data, headers=HEADERS, timeout=60)

        print(f"发送请求，正在访问第 {page_num} 页数据")

        # 2. 解析数据
        document = html.fromstring(response.text)
        movie_cards = document.xpath(
            '//div[contains(@class, "media-list-results")]/div[contains(@class, "rounded-xl")]'
        )
        print(f"获取到 {len(movie_cards)} 部电影")

        # 3. 遍历提取
        for card in movie_cards:
            href_list = card.xpath('.//a[contains(@href, "/movie/")]/@href')
            if href_list:
                movie_info_url = TMDB_BASE_URL + href_list[0]
                movie_info = get_movie_info(movie_info_url)
                all_movies.append(movie_info)

        print(f"第 {page_num} 页完成，累计 {len(all_movies)} 部")
        time.sleep(1)  # 防封

    # 4. 保存
    save_all_movies(all_movies)
    print(f"全部完成，共保存 {len(all_movies)} 部电影")

if __name__ == '__main__':
    main()