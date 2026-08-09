import  requests
import csv
from lxml import html

#常量
TMDB_BASE_URL = "https://www.themoviedb.org"
TMDB_TOP_URL = "https://www.themoviedb.org/movie/top-rated"

def save_all_movies(all_movies):
    pass

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
    # 1. 发送请求，获取高分电影榜单数据
    response = requests.get(TMDB_TOP_URL, timeout=60)

    # 2. 解析数据，获取电影列表
    document = html.fromstring(response.text)
    movie_list = document.xpath("//*[@id='page_1']/div/div/div[@class='w-full overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm transition-colors hover:border-gray-300']")
    # 3. 遍历电影列表，获取电影详情
    all_movies = []
    for movie in movie_list:
        movie_urls = movie.xpath("./div/div/a/@href")
        if movie_urls:
            # 电影详情中的url
            movie_info_url = TMDB_BASE_URL + movie_urls[0]
            # print(movie_info_url)
            # 发送请求，获取电影详情数据
            movie_info = get_movie_info(movie_info_url)
            all_movies.append(movie_info)

    # 4. 保存数据，保存为 csv 文件
    save_all_movies(all_movies)

#8/8
if __name__ == '__main__':
    main()