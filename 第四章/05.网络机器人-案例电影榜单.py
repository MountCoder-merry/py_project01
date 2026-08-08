import  requests
import csv
from lxml import html

#常量
TMDB_BASE_URL = "https://www.themoviedb.org"
TMDB_TOP_URL = "https://www.themoviedb.org/movie/top-rated"

def save_all_movies(all_movies):
    pass

def get_movie_info(movie_info_url):
    pass

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
            print(movie_info_url)
            # 发送请求，获取电影详情数据
            movie_info = get_movie_info(movie_info_url)
            all_movies.append(movie_info)

    # 4. 保存数据，保存为 csv 文件
    save_all_movies(all_movies)

#8/8
if __name__ == '__main__':
    main()