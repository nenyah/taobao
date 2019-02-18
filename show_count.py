import time

import pymongo

client = pymongo.MongoClient('localhost', 27017)
soyoung = client['soyoung']
page_urls = soyoung['page_urls']
detail_info = soyoung['detail_info']

while True:
	print(detail_info.find().count())
	time.sleep(30)