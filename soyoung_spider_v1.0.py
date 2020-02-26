#! /usr/bin/env python
# -*- coding:utf-8 -*-

import csv
import datetime
import logging
import os
import sys
from urllib.parse import urlencode

import requests
from selenium import webdriver

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s- %(message)s')
log = logging.info


def clean_text(text):
    return text.replace('\n', '').replace(' ', '')


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--log-level=3')
driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get("https://www.soyoung.com/")
cookies = driver.get_cookies()
MY_COOKIE = {}
for el in cookies:
    MY_COOKIE[el['name']] = el['value']
print(MY_COOKIE)
driver.quit()


class SoyoungSpider:
    """docstring for SoyoungSpider"""

    def __init__(self, keyword):
        self.keyword = keyword
        self.hospital_url = r'http://www.soyoung.com/searchNew/hospital?keyword={}&page={}'
        query = {'cityId': 1, 'page_size': 100, '_json': 1, 'sort': 3}
        self.hospital_url = self.hospital_url + '&' + urlencode(query)
        self.page = 1
        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'
        }
        self.item = []
        self.count = 1

    def get_info(self):
        url = self.hospital_url.format(self.keyword, self.page)
        r = requests.get(url, headers=self.headers, cookies=MY_COOKIE)
        hospitals = r.json()['responseData']['hospital_list']
        hasmore = r.json()['responseData']['has_more']
        for hospital in hospitals:
            for product in hospital['products']:
                if self.keyword in product['title']:
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
    if len(sys.argv) == 1:
        keyword = '伊婉'
    else:
        keyword = sys.argv[1]
    if os.name == 'nt':
        save_path = r'E:\玻尿酸销售情况'
    else:
        save_path = '/home/steven/sales_collect'
    spider = SoyoungSpider(keyword)
    spider.run()
    spider.save(save_path)


if __name__ == '__main__':
    main()
