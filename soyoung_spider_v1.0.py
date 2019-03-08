#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv
import datetime
import logging
import os
from urllib.parse import urlencode

import requests

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s- %(message)s')
log = logging.info


def clean_text(text):
    return text.replace('\n', '').replace(' ', '')


class SoyoungSpider:
    """docstring for SoyoungSpider"""

    def __init__(self, keyword):
        self.keyword = keyword
        self.hospital_url = r'http://www.soyoung.com/searchNew/hospital?keyword={}&page={}'
        query = {'cityId': 1, 'page_size': 100, '_json': 1, 'sort': 0}
        self.hospital_url = self.hospital_url + '&' + urlencode(query)
        self.page = 1
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
            'Cookie':
            '__order_time__=undefined; msg_time=undefined; back_order_time=undefined; complain_time=undefined; PHPSESSID=dc1427d4919f33cba167586ea4de82ad; __usersign__=1548055243342040070; __jsluid=8ad3fabbff0e8cf49e5913b2c557317f; Hm_lvt_b366fbb5465f5a86e1cc2871552e1fdb=1548055244; _ga=GA1.2.920844667.1548055244; _gid=GA1.2.1448278221.1548055244; __postion__=a%3A4%3A%7Bs%3A6%3A%22cityId%22%3Bs%3A3%3A%22176%22%3Bs%3A8%3A%22cityName%22%3Bs%3A9%3A%22%E5%AE%81%E6%B3%A2%E5%B8%82%22%3Bs%3A8%3A%22cityCode%22%3Bi%3A180%3Bs%3A3%3A%22jwd%22%3Bi%3A0%3B%7D; Hm_lpvt_b366fbb5465f5a86e1cc2871552e1fdb=1548055620; _gat=1'
        }
        self.item = []
        self.count = 1

    def get_info(self):
        url = self.hospital_url.format(self.keyword, self.page)
        r = requests.get(url, headers=self.headers)
        hospitals = r.json()['responseData']['hospital_list']
        hasmore = r.json()['responseData']['has_more']
        for hospital in hospitals:
            for product in hospital['products']:
                if '伊婉' in product['title']:
                    info = {
                        'hospital_id': hospital['hospital_id'],
                        'hospital': hospital['name_cn'],
                        'address': hospital['address'],
                        'title': product['title'],
                        'price': product['price_online'],
                        'link': 'http://y.soyoung.com/cp' + product['pid'],
                    }
                    self.item.append(info)
                    log(f"[+] {self.count} Start to download {info['link']}")
                    self.count += 1

        if hasmore:
            self.page += 1
            self.get_info()

    def save(self, save_path):
        log(f'[+] Total item: {len(self.item)}')
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        file = f'{today}{self.keyword}新氧销售情况.csv'
        path = os.path.join(save_path, file)
        log(f'[+] Start to save file to {path}')
        with open(path, "w+", newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'title', 'price', 'link', 'address', 'hospital', 'hospital_id'
                # 'phone'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in self.item:
                writer.writerow(row)
        log('[+] Save success')

    def run(self):
        self.get_info()


def main():
    keyword = '伊婉'
    if os.name == 'nt':
        save_path = r'E:\伊婉销售情况'
    else:
        save_path = '/home/steven/sales_collect'
    spider = SoyoungSpider(keyword)
    spider.run()
    spider.save(save_path)


if __name__ == '__main__':
    main()
