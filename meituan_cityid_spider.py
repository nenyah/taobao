from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
import re
import json
from settings import *


# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# browser = webdriver.Chrome(chrome_options=chrome_options)

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

print('开始爬去城市id')

try:
    url = 'http://www.meituan.com/changecity/'
    browser.get(url)
except TimeoutException:
    get_city_id(url)

html = browser.page_source
# print(html)
data = re.findall(r'window.AppData = (\{.+\})', html)[0]
# print(data)
data = json.loads(data)
items = data['openCityList']
print(items)
chs = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

with open('cityid.py', 'w') as f:
    f.write("city_id=[")
    for item in items:
        for info in item[1]:
            print(info['id'], info['name'])
            f.write('\"{0}\"=\"{1}\",\n'.format(info['id'], info['name']))
    f.write("]")


def get_city_id():
    """
    获取城市id
    :param url: 包含城市id的页面url
    """
    print('开始爬去城市id')

    try:
        url = 'http://www.meituan.com/changecity/'
        browser.get(url)
    except TimeoutException:
        get_city_id(url)

    html = browser.page_source
    print(html)
    data = re.findall(r'window.AppData = (\{.+\})', html)[0]
    # print(data)
    data = json.loads(data)
    items = data['openCityList']
    ch = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for ch in chs:
        for item in items[ch]:
            print(item['id'], item['name'])
            yield item['id'], item['name']


def main():
    # url = 'http://www.meituan.com/changecity/'
    get_city_id()


# if __name__ == '__main__':
#     main()


