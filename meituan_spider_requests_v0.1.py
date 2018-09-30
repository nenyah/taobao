import requests
import re
import json
from settings import *
import csv
import datetime
from cityid import city_id
import time
import random

KEYWORD = '玻尿酸'
_path = r"E:\伊婉销售情况"
today = datetime.date.today()
file = f'{_path}/{today}{KEYWORD}美团销售情况.csv'
header = ['link', 'hospital_name', 'title', 'price']


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


def parse(url):
    try:
        web = requests.get(url, headers=headers)
        time.sleep(random.randint(1, 5))
        web.encoding = 'utf-8'
        html = web.text
        data = re.findall(r'(\{.+\})', html)[0]
        data = json.loads(data)
        return data['data']
    except Exception as e:
        print('Error message:', e)


def get_totalcount(cid, url):
    try:
        totalcount = parse(url)['totalCount']
        return totalcount
    except:
        print(f'Error url is {url}')


def make_url(cid, limit):
    root_url = f'http://apimobile.meituan.com/group/v4/poi/pcsearch/{cid}/?offset=0&q={KEYWORD}'
    root_url += f'&limit={limit}'
    return root_url


def get_data(url):
    items = parse(url)['searchResult']
    for item in items:
        # print(item)
        if item['deals'] is not None:
            for deal in item['deals']:
                info = {'link': 'http://www.meituan.com/jiankangliren/' + str(item['id']) + '/',
                        'hospital_name': item['title'],
                        'title': deal['title'],
                        'price': deal['price']
                        }
                yield info


def main():
    with open(file, "w+", newline='', encoding='utf-8') as cf:
        writer = csv.writer(cf)
        writer.writerow(header)
        for cid, _ in sorted(city_id.items(), key=lambda d: len(d[0]))[:2000]:
            print(f'Start to crawl: {city_id[cid]}', end=' ')
            root_url = f'http://apimobile.meituan.com/group/v4/poi/pcsearch/{cid}/?offset=0&q={KEYWORD}'
            totalcount = get_totalcount(cid, root_url)
            if totalcount:
                print(f'Total data: {totalcount}')
                full_data_url = make_url(cid, totalcount)
                data = get_data(full_data_url)
                for info in data:
                    print(info)
                    writer.writerow(info.values())


if __name__ == '__main__':
    main()
