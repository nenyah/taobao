#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import datetime
import time
import random
import csv
import requests
from lxml import etree
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s- %(message)s')

log = logging.info


def clean_text(text):
    return text.replace('\n', '').replace(' ', '')


class YueMeiSpider:
    """docstring for YueMeiSpider"""

    def __init__(self, keyword):
        self.root = r'https://so.yuemei.com'
        self.keyword = keyword
        self.start_url = self.root + '/tao/' + self.keyword
        self.detail_url = set()
        self.item = []
        self.count = 0
        self.item_count = 0
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
            'Cookie': 'Hm_lvt_bbb28c93aca8fe7e95a44b2908aabce7=1533088179; \
            _yma=1533088179134; ym_onlyk=1533088179018217; \
            ym_onlyknew=15330881790268;\
             UM_distinctid=164f32d22a40-04a8fdf830feb6-47e1039-1fa400-164f32d22a614e; \
             gr_user_id=97cecb0b-791f-419a-936b-1aa584b61013; \
             YUEMEI=banpqs21vegk3u6lieahdq9336; \
             __jsluid=b4d08a0b9859d35429f2cc41dd014811; \
             CNZZDATA1253703185=1188495707-1533086270-https%253A%252F%252Fwww.yuemei.com%252F%7C1533086270;\
              Hm_lpvt_bbb28c93aca8fe7e95a44b2908aabce7=1533092051'
        }

    def __get(self, url):
        try:
            log(f'[+] {self.count} Start to get {url}')
            r = requests.get(url, headers=self.header)
            time.sleep(random.randint(1, 5))
            r.encoding = 'utf-8'
            self.count += 1
            return r.text
        except ConnectionError:
            log("Can't get page")

    def parse_url(self, response):
        tree = etree.HTML(response)
        urls = tree.xpath('//*[@class="taoItem _yma"]/@href')
        for url in urls:
            if url not in self.detail_url:
                self.detail_url.add(url)

        # 判断有没有下一页
        next_url = tree.xpath('//*[@class="next-page-btn"]/@href')

        if next_url:
            next_page_url = self.root + next_url[0]
            self.parse_url(self.__get(next_page_url))

    def parse_detal(self, url):
        log(f'[+] {self.item_count} Start to parse {url}')
        response = self.__get(url)
        tree = etree.HTML(response)
        title = self.__get_title(tree)
        price = self.__get_price(tree)
        link = url
        address = self.__get_address(tree)
        hospital = self.__get_hospital(tree)
        phone = self.__get_phone(tree)
        info = {
            'title': title,
            'price': price,
            'link': link,
            'address': address,
            'hospital': hospital,
            'phone': phone
        }
        self.item.append(info)
        self.item_count += 1

    def __get_title(self, tree):
        if tree is None:
            raise Exception("Null exception", tree)

        title_parent = tree.xpath('//div[@class="mainTit"]')[0]
        title = clean_text(title_parent.xpath('string(.)'))
        return title

    def __get_price(self, tree):
        if tree is None:
            raise Exception("Null exception", tree)
        price_node = tree.xpath(
            '//i[@class="ft36"]/text() | //*[@class="fs-20"]/text()')
        if price_node:
            price = clean_text(price_node[0])
            return price
        else:
            raise Exception("Null exception", tree)

    def __get_address(self, tree):
        if tree is None:
            raise Exception("Null exception", tree)
        address_node = tree.xpath(
            '//p[@class="item3"]/text()')
        if address_node:
            address = clean_text(address_node[0]).replace('地址：', '')
            return address
        return None

    def __get_hospital(self, tree):
        if tree is None:
            raise Exception("Null exception", tree)
        hospital_node = tree.xpath(
            '//p[@class="item1"]/a/text()')
        if hospital_node:
            hospital = clean_text(hospital_node[0])
            return hospital
        return None

    def __get_phone(self, tree):
        if tree is None:
            raise Exception("Null exception", tree)
        phone_node = tree.xpath(
            '//div[@class="hosInfo"]/p[last()]/text()')
        if phone_node:
            phone = clean_text(phone_node[0])
            return phone
        return None

    def crawl(self):
        self.parse_url(self.__get(self.start_url))
        while len(self.detail_url):
            detail_url = self.detail_url.pop()
            self.parse_detal(detail_url)

    def show_item(self):
        for item in self.item:
            log(item)

    def save(self, save_path):
        log(f'[+] Total downlaod: {self.count}')
        log(f'[+] Total item: {self.item_count}')

        file = datetime.datetime.today().strftime('%Y-%m-%d') + \
            f'{self.keyword}悦美销售情况.csv'
        path = os.path.join(save_path, file)
        log(f'[+] Start to save file to {path}')
        with open(path, "w+", newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title',
                          'price',
                          'link',
                          'address',
                          'hospital',
                          'phone']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in self.item:
                writer.writerow(row)
        log('[+] Save success')


def main():
    # 1. 创建一个爬虫
    # 2. 给爬虫一个关键词
    # 3. 爬虫运行
    # 4. 保存数据
    keyword = '伊婉'
    if os.name == 'nt':
        save_path = r'E:\伊婉销售情况'
    else:
        save_path = '/home/steven/sales_collect'
    spider = YueMeiSpider(keyword)
    spider.crawl()
    spider.save(save_path)


if __name__ == '__main__':
    main()
