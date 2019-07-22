import json
import re
import time
from urllib.parse import quote
import random

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from settings import *

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# browser = webdriver.Chrome(chrome_options=chrome_options)

browser = webdriver.Chrome()

wait = WebDriverWait(browser, 20)
KEYWORD = '伊婉'

urls = list()
db = client[MONGO_TAOBAO]


def index_page(page):
    """
    抓取索引页
    :param page: 页码
    """
    print('正在爬取第', page, '页')
    try:
        url = 'https://www.taobao.com/'
        product_url = 'https://s.taobao.com/search?q=' + \
            quote(KEYWORD) + '&bcoffset=12&s=' + str((page - 1) * 44)
        browser.get(url)
        time.sleep(random.randint(1,10))
        browser.get(product_url)
        wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'),
                str(page)))
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            '.m-itemlist .items .item')))
        get_products(page)
    except TimeoutException:
        index_page(page)


def get_products(page):
    """
    提取商品数据
    :param page: 页码
    """
    html = browser.page_source
    data = re.findall('g_page_config = (\{.+\})', html)[0]
    data = json.loads(data)
    items = data['mods']['itemlist']['data']['auctions']

    for item in items:
        print(item)

        save_to_mongo(item)


def save_to_mongo(result):
    """
    保存至MongoDB
    :param result: 结果
    """
    try:
        if db[MONGO_COLLECTION].insert(result):
            print('存储到MongoDB成功')
    except Exception:
        print('存储到MongoDB失败')


MAX_PAGE = 12


def main():
    """
    遍历每一页
    """
    for i in range(1, MAX_PAGE + 1):
        index_page(i)


if __name__ == '__main__':
    main()
