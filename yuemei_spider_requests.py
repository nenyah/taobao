import requests
import re
import datetime
import time
import random
from lxml import etree
import csv

KEYWORD = '伊婉'
_path = r"E:\伊婉销售情况"
today = datetime.date.today()
file = f'{_path}/{today}伊婉悦美销售情况.csv'
header = ['link', 'hospital_name', 'title', 'price']


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'so.yuemei.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
    'Cookie': 'Hm_lvt_bbb28c93aca8fe7e95a44b2908aabce7=1533088179; _yma=1533088179134; ym_onlyk=1533088179018217; ym_onlyknew=15330881790268; UM_distinctid=164f32d22a40-04a8fdf830feb6-47e1039-1fa400-164f32d22a614e; gr_user_id=97cecb0b-791f-419a-936b-1aa584b61013; YUEMEI=banpqs21vegk3u6lieahdq9336; __jsluid=b4d08a0b9859d35429f2cc41dd014811; CNZZDATA1253703185=1188495707-1533086270-https%253A%252F%252Fwww.yuemei.com%252F%7C1533086270; Hm_lpvt_bbb28c93aca8fe7e95a44b2908aabce7=1533092051'
}


def parse(url):
    try:
        web = requests.get(url, headers=headers)
        time.sleep(random.randint(1, 5))
        web.encoding = 'utf-8'
        html = web.text
        # print(html)
        tree = etree.HTML(html)
        return tree
    except Exception as e:
        print('Error message:', e)


def get_totalcount(url):
    totalcount = int(parse(url).xpath('//*[@class="all-num"]/i/text()')[0])
    return totalcount


def make_url(totalcount):
    url = (f'https://so.yuemei.com/tao/{KEYWORD}/p{str(page)}.html' for page in range(1, totalcount + 1)
           )
    return url


def get_data(url):
    items = parse(url).xpath('//a[@class="taoItem _yma"]')
    for item in items:
        info = {'link': item.xpath('./@href')[0],
                'hospital_name': item.xpath(
            './/p[@class="listInfo-item4"]/text()')[0].strip(),
            'title': item.xpath(
            './/p[@class="listInfo-item2"]/text()')[0].strip(),
            'price': _get_price(item)
        }
        yield info


def _get_price(tree):
    price = tree.xpath('.//p[@class="ymPrice"]')[0]
    return re.sub(r'\n| ', '', price.xpath('string(.)'))


def main():
    with open(file, "w+", newline='', encoding='utf-8') as cf:
        writer = csv.writer(cf)
        writer.writerow(header)
        root_url = 'https://so.yuemei.com/tao/%E4%BC%8A%E5%A9%89/p1.html'
        totalcount = get_totalcount(root_url)
        page_count = 1
        info_count = 1
        for url in make_url(totalcount):
            print(f'[+] {page_count} Start to crawl: {url}')
            page_count += 1
            data = get_data(url)
            for info in data:
                print(f'[+] {info_count}:')
                print(info)
                writer.writerow(info.values())
                info_count += 1


if __name__ == '__main__':
    main()
