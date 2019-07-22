import requests
import re
import json
from settings import *
import csv
import datetime
from cityid import city_id
import time
import random

KEYWORD = '伊婉'
_path = r"E:\玻尿酸销售情况"
today = datetime.date.today()
file = f'{_path}/{today}{KEYWORD}美团销售情况.csv'
header = ['link', 'hospital_name', 'title', 'price']


cookies = {
    'uuid': 'cc8ed087f0c644b1a952.1557453915.1.0.0',
    'ci': '1',
    'rvct': '1',
    '_lxsdk_cuid': '16a9f7cc670c8-0257a980e49025-6353160-1fa400-16a9f7cc670c8',
    'IJSESSIONID': '1xknnzerz80ha1shooh8o9443a',
    'iuuid': 'AF69710FC465CDE9BAD8F1B96074D1A93F5E4B20B5B1C9EC91216B0E20FEBFA7',
    'cityname': '%E5%8C%97%E4%BA%AC',
    '_lxsdk': 'AF69710FC465CDE9BAD8F1B96074D1A93F5E4B20B5B1C9EC91216B0E20FEBFA7',
    'i_extend': 'H__a100005__b1',
    'idau': '1',
    'webp': '1',
    '__utma': '74597006.1819138348.1557453923.1557453923.1557453923.1',
    '__utmc': '74597006',
    '__utmz': '74597006.1557453923.1.1.utmcsr=bj.meituan.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
    '_lx_utm': 'utm_source%3Dbj.meituan.com%26utm_medium%3Dreferral%26utm_content%3D%252F',
    'latlng': '29.905372,121.793089,1557454258010',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    'DNT': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
}

params = (
    ('offset', '0'),
    ('q', '\u4F0A\u5A49'),
)

response = requests.get('http://apimobile.meituan.com/group/v4/poi/pcsearch/1/', headers=headers, params=params, cookies=cookies)

print(response.json())


# def parse(url):
#     try:
#         web = requests.get(url, headers=headers)
#         time.sleep(random.randint(1, 5))
#         web.encoding = 'utf-8'
#         html = web.text
#         data = re.findall(r'(\{.+\})', html)[0]
#         data = json.loads(data)
#         return data['data']
#     except Exception as e:
#         print('Error message:', e)


# def get_totalcount(cid, url):
#     try:
#         totalcount = parse(url)['totalCount']
#         return totalcount
#     except:
#         print(f'Error url is {url}')


# def make_url(cid, limit):
#     root_url = f'http://apimobile.meituan.com/group/v4/poi/pcsearch/{cid}/?offset=0&q={KEYWORD}'
#     root_url += f'&limit={limit}'
#     return root_url


# def get_data(url):
#     items = parse(url)['searchResult']
#     for item in items:
#         # print(item)
#         if item['deals'] is not None:
#             for deal in item['deals']:
#                 info = {'link': 'http://www.meituan.com/jiankangliren/' + str(item['id']) + '/',
#                         'hospital_name': item['title'],
#                         'title': deal['title'],
#                         'price': deal['price']
#                         }
#                 yield info


# def main():
#     with open(file, "w+", newline='', encoding='utf-8') as cf:
#         writer = csv.writer(cf)
#         writer.writerow(header)
#         for cid, _ in sorted(city_id.items(), key=lambda d: len(d[0]))[:2000]:
#             print(f'Start to crawl: {city_id[cid]}', end=' ')
#             root_url = f'http://apimobile.meituan.com/group/v4/poi/pcsearch/{cid}/?offset=0&q={KEYWORD}'
#             totalcount = get_totalcount(cid, root_url)
#             if totalcount:
#                 print(f'Total data: {totalcount}')
#                 full_data_url = make_url(cid, totalcount)
#                 data = get_data(full_data_url)
#                 for info in data:
#                     print(info)
#                     writer.writerow(info.values())


# if __name__ == '__main__':
#     main()
