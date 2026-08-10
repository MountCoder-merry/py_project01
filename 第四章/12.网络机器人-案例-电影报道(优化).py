import time
import requests
import csv
import re
from lxml import html

# 常量
MOVIE_LIST_FILE = "csv_data/movie_list2.csv"
TMDB_BASE_URL = "https://www.themoviedb.org"
TMDB_TOP_URL_1 = "https://www.themoviedb.org/movie/top-rated"
TMDB_TOP_URL_2 = "https://www.themoviedb.org/discover/movie/items"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://www.themoviedb.org/",
}


def save_all_movies(all_movies):
    """保存所有电影数据到CSV文件"""
    with open(MOVIE_LIST_FILE, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile,
                                fieldnames=["电影名", "年份", "上映时间", "类型", "时长", "评分", "语言", "导演",
                                            "作者", "宣传语", "简介"])
        writer.writeheader()
        writer.writerows(all_movies)


def get_movie_year(movie_years):
    """获取电影年份，去除括号"""
    movie_year = movie_years[0].strip() if movie_years else ''
    return movie_year.replace("(", "").replace(")", "").strip()


def get_movie_publish_date(movie_dates):
    """获取电影上映时间，提取日期格式 YYYY-MM-DD"""
    movie_date = movie_dates[0].strip() if movie_dates else ''
    if movie_date:
        result = re.search(r"\d{4}-\d{2}-\d{2}", movie_date)
        return result.group() if result else ''
    return ''


def get_movie_cost_time(movie_cost_times):
    """获取电影时长，统一转换为分钟"""
    movie_cost_time = movie_cost_times[0].strip() if movie_cost_times else ''
    if not movie_cost_time:
        return ''

    total_minutes = 0

    # 提取小时
    h_match = re.search(r"(\d+)h", movie_cost_time)
    if h_match:
        total_minutes += int(h_match.group(1)) * 60

    # 提取分钟
    m_match = re.search(r"(\d+)m", movie_cost_time)
    if m_match:
        total_minutes += int(m_match.group(1))

    # 如果只有单独的数字，可能表示分钟
    if not h_match and not m_match:
        num_match = re.search(r"(\d+)", movie_cost_time)
        if num_match:
            total_minutes = int(num_match.group(1))

    return f"{total_minutes}分钟" if total_minutes > 0 else ''


def get_movie_info(movie_info_url):
    """获取单个电影的详细信息"""
    try:
        movie_response = requests.get(movie_info_url, headers=HEADERS, timeout=60)
        movie_response.raise_for_status()
    except requests.RequestException as e:
        print(f"获取电影详情失败: {movie_info_url}, 错误: {e}")
        return None

    # 解析数据
    movie_doc = html.fromstring(movie_response.text)

    # 提取各项信息（使用更灵活的XPath）
    movie_names = movie_doc.xpath("//h2/a/text() | //*[@id='original_header']//h2/a/text()")
    movie_years = movie_doc.xpath("//h2/span/text() | //*[@id='original_header']//h2/span/text()")
    movie_dates = movie_doc.xpath(
        "//*[@id='original_header']//div[contains(@class, 'info')]/span[2]/text() | //*[contains(text(), '上映')]/following-sibling::text()")
    movie_tags = movie_doc.xpath(
        "//*[@id='original_header']//span[contains(@class, 'genres')]/a/text() | //a[contains(@href, '/genre/')]/text()")
    movie_cost_times = movie_doc.xpath(
        "//*[@id='original_header']//span[contains(text(), 'h') or contains(text(), 'm')]/text() | //*[contains(text(), '分钟')]/text()")

    # 评分
    movie_scores = movie_doc.xpath(
        "//*[@id='consensus_pill']//div/@data-percent | //*[contains(@class, 'score')]/@data-percent")

    # 语言
    movie_languages = movie_doc.xpath(
        "//*[@id='media_v4']//p[contains(text(), '语言')]/following-sibling::text() | //*[contains(text(), '语言')]/following-sibling::text()")

    # 导演
    movie_directors = movie_doc.xpath(
        "//*[contains(text(), '导演')]/following-sibling::a/text() | //*[@id='original_header']//li[1]/p[1]/a/text()")

    # 作者
    movie_authors = movie_doc.xpath(
        "//*[contains(text(), '作者')]/following-sibling::a/text() | //*[@id='original_header']//li[2]/p[1]/a/text()")

    # 宣传语
    movie_slogans = movie_doc.xpath(
        "//*[@id='original_header']//h3[contains(@class, 'tagline')]/text() | //*[contains(@class, 'tagline')]/text()")

    # 简介
    movie_descriptions = movie_doc.xpath(
        "//*[@id='original_header']//div[contains(@class, 'overview')]/p/text() | //*[contains(@class, 'overview')]/text()")

    # 处理特殊字段
    year = get_movie_year(movie_years)
    publish_date = get_movie_publish_date(movie_dates)
    cost_time = get_movie_cost_time(movie_cost_times)

    movie_info = {
        "电影名": movie_names[0].strip() if movie_names else '',
        "年份": year,
        "上映时间": publish_date,
        "类型": ", ".join([tag.strip() for tag in movie_tags if tag.strip()]) if movie_tags else '',
        "时长": cost_time,
        "评分": movie_scores[0].strip() if movie_scores else '',
        "语言": movie_languages[0].strip() if movie_languages else '',
        "导演": ", ".join(
            [director.strip() for director in movie_directors if director.strip()]) if movie_directors else '',
        "作者": ", ".join([author.strip() for author in movie_authors if author.strip()]) if movie_authors else '',
        "宣传语": movie_slogans[0].strip() if movie_slogans else '',
        "简介": movie_descriptions[0].strip() if movie_descriptions else ''
    }

    print(f"✓ 获取电影: {movie_info['电影名']} ({movie_info['年份']})")
    return movie_info


def main():
    """主函数"""
    all_movies = []

    for page_num in range(1, 6):
        try:
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

            response.raise_for_status()
            print(f"发送请求，正在访问第 {page_num} 页数据")

            # 2. 解析数据
            document = html.fromstring(response.text)

            # 多种方式尝试获取电影卡片
            movie_cards = document.xpath(
                '//div[contains(@class, "media-list-results")]/div[contains(@class, "rounded-xl")]'
            )

            if not movie_cards:
                # 备用选择器
                movie_cards = document.xpath('//div[contains(@class, "media-card")]')

            if not movie_cards:
                # 通过链接查找
                movie_links = document.xpath('//a[contains(@href, "/movie/")]')
                movie_cards = []
                for link in movie_links:
                    parent = link.getparent()
                    while parent is not None:
                        if parent.tag == 'div' and (
                                'card' in parent.get('class', '').lower() or 'media' in parent.get('class',
                                                                                                   '').lower()):
                            movie_cards.append(parent)
                            break
                        parent = parent.getparent()

            print(f"获取到 {len(movie_cards)} 部电影")

            # 3. 遍历提取
            for idx, card in enumerate(movie_cards, 1):
                href_list = card.xpath('.//a[contains(@href, "/movie/")]/@href')
                if href_list:
                    movie_info_url = TMDB_BASE_URL + href_list[0]
                    print(f"  [{idx}/{len(movie_cards)}] 获取详情: {movie_info_url}")
                    movie_info = get_movie_info(movie_info_url)
                    if movie_info:  # 只添加成功获取的
                        all_movies.append(movie_info)
                    time.sleep(0.5)  # 避免请求过快

            print(f"第 {page_num} 页完成，累计 {len(all_movies)} 部")
            time.sleep(1)  # 防封

        except requests.RequestException as e:
            print(f"请求第 {page_num} 页失败: {e}")
            continue
        except Exception as e:
            print(f"处理第 {page_num} 页时发生错误: {e}")
            continue

    # 4. 保存
    if all_movies:
        save_all_movies(all_movies)
        print(f"✅ 全部完成，共保存 {len(all_movies)} 部电影到 {MOVIE_LIST_FILE}")
    else:
        print("❌ 没有获取到任何电影数据")


if __name__ == '__main__':
    main()