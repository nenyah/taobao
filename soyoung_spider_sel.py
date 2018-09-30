import json
import os
import csv
import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from lxml import etree


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)

# browser = webdriver.Chrome()
# wait = WebDriverWait(browser, 10)

page = 1
flag = True
products = set()
infos = []

while flag:
    try:
        url = f'http://www.soyoung.com/searchNew/product?keyword=%E4%BC%8A%E5%A9%89&cityId=176&page_size=12&_json=1&sort=0&service=&coupon=&group=&maxprice=&minprice=&page={page}'
        browser.get(url)
        html = browser.page_source
        tree = etree.HTML(html)
        # print(html)
        data = json.loads(tree.xpath('//pre/text()')[0])
        arr_product = data['responseData']['arr_product']
        if arr_product:
            for product in arr_product:
                p_url = 'http://y.soyoung.com/cp' + product['pid']
                print(p_url)
                products.add(p_url)
            page += 1
        else:
            flag = False
    except Exception as e:
        raise e

while len(products):
    p_url = products.pop()
    print(f'Parse {p_url}')
    browser.get(p_url)
    html = browser.page_source
    tree = etree.HTML(html)

    title = tree.xpath('//h1/text()')
    price = tree.xpath('//*[@id="baseInfo"]/div/em/text()')
    hospital = tree.xpath('//*[@class="hospital-logo"]/p/text()')
    address = tree.xpath('//*[@class="hospital"]//tr[3]/td[2]/text()')
    phone = tree.xpath('//*[@class="hospital"]//tr[4]/td[2]/text()')
    info = {
        'title': title[0] if title else None,
        'link': p_url,
        'price': price[0] if price else None,
        'hospital': hospital[0] if hospital else None,
        'address': address[0] if address else None,
        'phone': phone[0] if phone else None}
    print(info)
    infos.append(info)

if os.name == 'nt':
    save_path = r'E:\伊婉销售情况'
else:
    save_path = '/home/steven/sales_collect'
file = datetime.datetime.today().strftime('%Y-%m-%d') + '伊婉新氧销售情况.csv'
path = os.path.join(save_path, file)
with open(path, "w+", newline='', encoding='utf-8') as csvfile:
    fieldnames = ['title',
                  'price',
                  'link',
                  'address',
                  'hospital',
                  'phone']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in infos:
        writer.writerow(row)
