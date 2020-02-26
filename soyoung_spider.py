#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv
import datetime
import logging
import os
import itertools

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
        self.root = 'http://www.soyoung.com/searchNew/'
        self.product_url = self.root + \
            r'product?keyword={}&cityId=1&page_size=100&_json=1&sort=0&page={}'
        self.hospital_url = self.root + \
            r'hospital?keyword={}&cityId=1&page_size=100&_json=1&sort=0&page={}'
        self.page = 1
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
            'Cookie':
            '__order_time__=undefined; msg_time=undefined; back_order_time=undefined; complain_time=undefined; PHPSESSID=dc1427d4919f33cba167586ea4de82ad; __usersign__=1548055243342040070; __jsluid=8ad3fabbff0e8cf49e5913b2c557317f; Hm_lvt_b366fbb5465f5a86e1cc2871552e1fdb=1548055244; _ga=GA1.2.920844667.1548055244; _gid=GA1.2.1448278221.1548055244; __postion__=a%3A4%3A%7Bs%3A6%3A%22cityId%22%3Bs%3A3%3A%22176%22%3Bs%3A8%3A%22cityName%22%3Bs%3A9%3A%22%E5%AE%81%E6%B3%A2%E5%B8%82%22%3Bs%3A8%3A%22cityCode%22%3Bi%3A180%3Bs%3A3%3A%22jwd%22%3Bi%3A0%3B%7D; Hm_lpvt_b366fbb5465f5a86e1cc2871552e1fdb=1548055620; _gat=1'
        }
        self.item = []
        self.hospitals = []
        self.count = 1

    def get_base_info(self):
        url = self.product_url.format(self.keyword, self.page)
        r = requests.get(url, headers=self.headers)
        hasmore = r.json()['responseData']['has_more']
        products = r.json()['responseData']['arr_product']
        for product in products:
            info = {
                'link': 'http://y.soyoung.com/cp' + product['pid'],
                'hospital': product['hospital_name'],
                'title': product['title'],
                'price': product['price_online'],
                'hospital_id': product['hospital_id']
            }
            self.item.append(info)
            log(f"[+] {self.count} Start to download {info['link']}")
            self.count += 1

        if hasmore:
            self.page += 1
            self.get_base_info()

    def get_hospital_info(self):
        url = self.hospital_url.format(self.keyword, self.page)
        r = requests.get(url, headers=self.headers)
        hospitals = r.json()['responseData']['hospital_list']
        hasmore = r.json()['responseData']['has_more']
        for hospital in hospitals:
            info = {
                'hospital_id': hospital['hospital_id'],
                'address': hospital['address']
            }
            self.hospitals.append(info)

        if hasmore:
            self.page += 1
            self.get_hospital_info()

    def match_address(self):
        for hospital, product in itertools.product(self.hospitals,
                                                   self.item.copy()):
            if hospital['hospital_id'] == product['hospital_id']:
                self.item.remove(product)
                product['address'] = hospital['address']
                self.item.append(product)

    def save(self, save_path):
        log(f'[+] Total item: {len(self.item)}')

        file = datetime.datetime.today().strftime('%Y-%m-%d') + \
            f'{self.keyword}新氧销售情况.csv'
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

    def run(self, save_path):
        self.get_hospital_info()
        self.get_base_info()
        self.match_address()
        self.save(save_path)


def main():
    keyword = '伊婉'
    if os.name == 'nt':
        save_path = r'E:\玻尿酸销售情况'
    else:
        save_path = '/home/steven/sales_collect'
    spider = SoyoungSpider(keyword)
    spider.run(save_path)


if __name__ == '__main__':
    main()
