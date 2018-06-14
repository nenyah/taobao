from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
import re
import json
from settings import *
import time


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)

# browser = webdriver.Chrome()

wait = WebDriverWait(browser, 20)
KEYWORD = '伊婉'


db = client[MONGO_MEITUAN]

MAX_PAGE = 100


def save_to_mongo(result):
    """
    保存至MongoDB
    :param result: 结果
    """
    try:
        if db[MONGO_COLLECTION].insert(result):
            print('存储到MongoDB成功')
    except Exception as e:
        print('存储到MongoDB失败:', e)


def save_data(items):
    """
    把产品信息存入数据库
    :param items: 待解析item
    """
    for item in items:
        if item['deals'] is not None:
            for deal in item['deals']:
                info = {'store_url': 'http://www.meituan.com/jiankangliren/' + str(item['id']) + '/',
                        'store_name': item['title'],
                        'product_name': deal['title'],
                        'price': deal['price']
                        }
                print(info)
                save_to_mongo(item)


def get_product(city_id):
    """
    获取产品信息
    :param city_id: 城市编号
    :param page: 页码
    """
    print(f'正在爬取城市编号{city_id}')
    time.sleep(5)
    EXISTS_DATA = True
    page = 1

    while EXISTS_DATA and page < 3:
        try:
            print(f'正在爬取第{page}页')
            url = 'http://apimobile.meituan.com/group/v4/poi/pcsearch/' + str(city_id) + '?limit=32&offset=' + \
                str((page - 1) * 32) + '&q=' + quote(KEYWORD)
            print(url)
            browser.get(url)

        except TimeoutException:
            get_product_by_page(city_id, page)

        html = browser.page_source

        data = re.findall(r'(\{.+\})', html)[0]
        # print(data)
        data = json.loads(data)
        items = data['data']['searchResult']
        if len(items) == 0:
            # raise Exception("No data")
            print("No data")
            EXISTS_DATA = False
        else:
            page += 1
            save_data(items)


def get_product_by_city(city_id):
    """
    按城市编号获取产品信息
    :param city_id: 城市编号
    """

    try:
        get_product(city_id)
    except:
        raise Exception(f"can't parse {city_id}")


def get_city_id_list(file='./cityid.txt'):
    with open(file, 'r') as f:
        content = f.readlines()
        for line in content:
            _id = line.split(',')[0]
            yield _id


def main():
    """
    遍历每一页
    """
    for city_id in get_city_id_list():
        get_product_by_city(city_id)


def test():
    city_id = 10
    get_product_by_city(city_id)


if __name__ == '__main__':
    main()
    # test()
    # print(list(get_city_id_list()))
