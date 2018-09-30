#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import datetime
import csv
import requests
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s- %(message)s')
log = logging.info


def clean_text(text):
    return text.replace('\n', '').replace(' ', '')


class SoyoungSpider:
    """docstring for SoyoungSpider"""

    def __init__(self, keyword):
        self.keyword = keyword
        self.product_url = r'http://www.soyoung.com/searchNew/product'
        self.hospital_url = r'http://www.soyoung.com/searchNew/hospital'
        self.params = {
            'keyword': keyword,
            'cityId': '1',
            '_json': '1',
            'page_size': '3000',
            'page': '1',
            'sort': '0',
            'service': None,
            'coupon': None,
            'group': None,
            'maxprice': None,
            'minprice': None
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
            'Cookie': '__usersign__=1535530192535864254;\
             _ga=GA1.2.761995634.1535530645;\
             __jsluid=42a69d7898afb3425ce34bc3e9498dbf;\
              __order_time__=undefined; \
             msg_time=undefined; back_order_time=undefined; \
             PHPSESSID=8b40626848426e8617b23acac65e82ce;\
              __postion__=a%3A4%3A%7Bs%3A6%3A%22cityId%22%3Bs%3A3%3A%22176%22%3Bs%3A8%3A%22cityName%22%3Bs%3A9%3A%22%E5%AE%81%E6%B3%A2%E5%B8%82%22%3Bs%3A8%3A%22cityCode%22%3Bi%3A180%3Bs%3A3%3A%22jwd%22%3Bi%3A0%3B%7D;\
               _gid=GA1.2.258180470.1537171632; \
               Hm_lvt_b366fbb5465f5a86e1cc2871552e1fdb=1535530645,1537171632; \
               Hm_lpvt_b366fbb5465f5a86e1cc2871552e1fdb=1537171632'
        }
        self.item = []
        self.count = 1

    def get_base_info(self, url):
        r = requests.get(url, params=self.params, headers=self.headers)
        products = r.json()['responseData']['arr_product']
        for product in products:
            info = {}
            info['link'] = 'http://y.soyoung.com/cp' + product['pid']
            info['hospital'] = product['hospital_name']
            info['title'] = product['title']
            info['price'] = product['price_online']
            info['hospital_id'] = product['hospital_id']
            self.item.append(info)
            log(f"[+] {self.count} Start to download {info['link']}")
            self.count += 1

    def get_hospital_info(self, url):
        r = requests.get(url, params=self.params, headers=self.headers)
        hospitals = r.json()['responseData']['hospital_list']
        for hospital in hospitals:
            for index in range(len(self.item)):
                if hospital['hospital_id'] == self.item[index]['hospital_id']:
                    self.item[index]['address'] = hospital['address']

    def save(self, save_path):
        log(f'[+] Total item: {len(self.item)}')

        file = datetime.datetime.today().strftime('%Y-%m-%d') + f'{self.keyword}新氧销售情况.csv'
        path = os.path.join(save_path, file)
        log(f'[+] Start to save file to {path}')
        with open(path, "w+", newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title',
                          'price',
                          'link',
                          'address',
                          'hospital',
                          'hospital_id'
                          # 'phone'
                          ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in self.item:
                writer.writerow(row)
        log('[+] Save success')

    def run(self):
        self.get_base_info(self.product_url)
        self.get_hospital_info(self.hospital_url)


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
