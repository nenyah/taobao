import requests
import re
import json
import pandas
from settings import *
from urllib.parse import quote
from cityid import city_id
KEYWORD = '伊婉'


db = client[MONGO_MEITUAN]
root_url = 'http://apimobile.meituan.com/group/v4/poi/pcsearch/'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'apimobile.meituan.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
}


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
                save_to_mongo(info)


def parse(web):
    """
    解析网页
    :param web: requests返回的网页
    """
    html = web.text

    data = re.findall(r'(\{.+\})', html)[0]
    data = json.loads(data)
    items = data['data']['searchResult']
    return items


def make_url(city_id, page, keyword):
    return f'{root_url}{str(city_id)}?limit=32&offset={str((page - 1) * 32)}&q={quote(KEYWORD)}'


def get_product(city_id):
    """
    获取产品信息
    :param city_id: 城市编号
    :param page: 页码
    """
    print(f'正在爬取城市编号{city_id}')
    EXISTS_DATA = True
    page = 1

    while EXISTS_DATA:
        try:
            print(f'正在爬取第{page}页')
            url = 'http://apimobile.meituan.com/group/v4/poi/pcsearch/' + str(city_id) + '?limit=32&offset=' + \
                str((page - 1) * 32) + '&q=' + quote(KEYWORD)
            print(url)
            web = requests.get(url, headers=headers)
            # print(web.status_code)

        except:
            print('wrong when get')
            EXISTS_DATA = False
            # get_product(city_id)

        if web.status_code == 200:
            items = parse(web)
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


def main():
    """
    遍历每一页
    """
    for _id in city_id.keys():
        get_product_by_city(_id)


def test():
    city_id = 10
    get_product_by_city(city_id)


if __name__ == '__main__':
    main()
    # test()
    # print(list(get_city_id_list()))
