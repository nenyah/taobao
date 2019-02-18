import requests
from selenium import webdriver
import time
import pandas as pd
import pymongo

MONGO_URL = 'localhost'
MONGO_DB = 'latitude'
MONGO_COLLECTION = 'lat'
client = pymongo.MongoClient(MONGO_URL, 27017)
db = client[MONGO_DB]


def save_to_mongo(result):
    try:
        if db[MONGO_COLLECTION].insert(result):
            print('存储到MongoDB成功')
    except Exception as e:
        print('存储到MongoDB失败')


def get_lat_and_lng(address):
    url = r"http://api.map.baidu.com/cloudgc/v1?"
    params = {'ak': '*******', 'address': address}
    try:
        r = requests.get(url, params=params)
        return r.json()['result']['location']
    except Exception as e:
        raise e


path = r"F:\steven\Documents\WXWork Files\File\2018-11\华东宁波医药无经纬度机构20181126.xlsx"
df = pd.read_excel(path)


def get_lat(web, address):
    input_text = web.find_element_by_xpath('//*[@id="s_t"]')
    submit_button = web.find_element_by_xpath('//*[@id="s_btn"]')
    input_text.clear()
    input_text.send_keys(address)
    time.sleep(1)
    submit_button.click()
    time.sleep(5)

    lat = web.find_element_by_xpath('//*[@id="curr_xy"]').text

    return lat


def get_result(df):
    result = []
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--headless')
    web = webdriver.Chrome(chrome_options=chrome_options)
    url = 'http://www.gpsspg.com/maps.htm'
    web.get(url)

    for InstitutionID, name, add in zip(df['InstitutionID'],
                                        df['InstitutionName'], df['Address']):
        if not pd.isna(add):

            info = {
                'InstitutionID': InstitutionID,
                'Address': add,
                'lat': get_lat(web, add)
            }
            print(info)
            save_to_mongo(info)
        else:

            info = {
                'InstitutionID': InstitutionID,
                'Address': None,
                'lat': get_lat(web, name)
            }
            print(info)
            save_to_mongo(info)
        result.append(info)

    web.close()
    return pd.DataFrame(result)


out = get_result(df)
out.to_csv('match_lat.csv', index=False)
