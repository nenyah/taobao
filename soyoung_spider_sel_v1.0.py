import csv
import datetime
import json
import logging
import os
import time
import urllib

import pandas as pd
import pymongo
from lxml import etree
from selenium import webdriver

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s- %(message)s')
log = logging.info


def start_chrome():
    """开启chrome"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver


driver = start_chrome()
# browser = webdriver.Chrome()
# wait = WebDriverWait(browser, 10)
client = pymongo.MongoClient('localhost', 27017)
soyoung = client['soyoung']
page_urls = soyoung['page_urls']
detail_info = soyoung['detail_info']

mongo_start = True


def get_detail_url(url: str) -> set:
    '''从搜索目录中获取详情页链接
    @param url 搜索目录根地址
    @return products 所有详情页链接
    '''
    products = set()
    page = 1
    flag = True
    while flag:
        try:
            params = {
                'keyword': '伊婉',
                'cityId': 176,
                'page_size': 12,
                '_json': 1,
                'sort': 0,
                'service': '',
                'coupon': '',
                'group': '',
                'maxprice': '',
                'minprice': '',
                'page': page
            }
            url = url + '?' + urllib.parse.urlencode(params)
            log(url)
            driver.get(url)
            time.sleep(3)
            html = driver.page_source
            tree = etree.HTML(html)
            # log(html)
            data = json.loads(tree.xpath('//pre/text()')[0])
            arr_product = data['responseData']['arr_product']
            if arr_product:
                for product in arr_product:
                    link = 'http://y.soyoung.com/cp' + product['pid']
                    log(link)
                    if mongo_start:
                        page_urls.insert_one({'link': link})
                    products.add(link)
                page += 1
            else:
                flag = False
        except Exception as e:
            pass
    return products


def get_detail_info(url: str) -> dict:
    '''获取详情信息
    @param url str 详情页链接
    @return info dict 获取信息
    '''
    try:
        time.sleep(3)
        driver.get(url)
    except Exception as e:
        return
    html = driver.page_source
    tree = etree.HTML(html)

    title = tree.xpath('//h1/text()')
    price = tree.xpath('//*[@id="baseInfo"]/div/em/text()')
    hospital = tree.xpath('//*[@class="hospital-logo"]/p/text()')
    address = tree.xpath('//*[@class="hospital"]//tr[3]/td[2]/text()')
    phone = tree.xpath('//*[@class="hospital"]//tr[4]/td[2]/text()')
    if title:
        info = {
            'title': title[0],
            'link': url,
            'price': price[0] if price else None,
            'hospital': hospital[0] if hospital else None,
            'address': address[0] if address else None,
            'phone': phone[0] if phone else None,
            'crawl_date': datetime.datetime.today()
        }
        if mongo_start:
            detail_info.insert_one(info)
        log(info)
        return info


def to_csv(infos: list):
    '''存储到csv文件'''
    if os.name == 'nt':
        save_path = r'E:\伊婉销售情况'
    else:
        save_path = '/home/steven/sales_collect'
    file = datetime.datetime.today().strftime('%Y-%m-%d') + '伊婉新氧销售情况.csv'
    path = os.path.join(save_path, file)
    with open(path, "w+", newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'title', 'price', 'link', 'address', 'hospital', 'phone',
            'crawl_date'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in infos:
            writer.writerow(row)


def mongo_to_csv():
    '''存储到csv文件'''
    if os.name == 'nt':
        save_path = r'E:\伊婉销售情况'
    else:
        save_path = '/home/steven/sales_collect'
    file = datetime.datetime.today().strftime('%Y-%m-%d') + '伊婉新氧销售情况.csv'
    path = os.path.join(save_path, file)

    df = pd.DataFrame(detail_info.find())
    df.to_csv(path, index=False)


def get_all_detail_by_mongo(wait_for_crawl):

    for link in list(wait_for_crawl):
        log(f'Parse {link}')
        get_detail_info(link)


def get_all_detail(urls: list) -> list:
    ''' 抓取所有产品页详情信息'''

    infos = []
    while len(urls):
        p_url = urls.pop()
        log(f'Parse {p_url}')
        info = get_detail_info(p_url)
        infos.append(info)
    return infos


if __name__ == "__main__":
    url = 'http://www.soyoung.com/searchNew/product'

    if mongo_start:
        if list(detail_info.find()):
            crawled = set(info['link'] for info in detail_info.find({}, {
                "link": 1,
                "_id": 0
            }))
        else:
            crawled = set()
        if list(page_urls.find()):
            all_urls = set(info['link'] for info in page_urls.find({}, {
                "link": 1,
                "_id": 0
            }))
        else:
            get_detail_url(url)
            all_urls = set(info['link'] for info in page_urls.find({}, {
                "link": 1,
                "_id": 0
            }))
        wait_for_crawl = all_urls - crawled
        get_all_detail_by_mongo(wait_for_crawl)
        mongo_to_csv()
    else:
        products = get_detail_url(url)
        infos = get_all_detail(products)
        to_csv(infos)
