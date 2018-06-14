import pandas as pd
import datetime
from settings import *

today = datetime.date.today()
db_meituan = client[MONGO_MEITUAN]

db_taobao = client[MONGO_TAOBAO]


def main():
    tb_df = pd.DataFrame(list(db_taobao[MONGO_COLLECTION].find()))
    tb_export_df = tb_df.loc[:, ['raw_title',
                                 'detail_url', 'view_price', 'nick']]
    tb_export_df.columns = ['标题', '链接', '价格', '旺旺']
    tb_export_df.to_csv(f'E:/{today}伊婉淘宝销售情况.csv', index=False)
    mt_df = pd.DataFrame(list(db_meituan[MONGO_COLLECTION].find()))
    mt_export_df = mt_df.loc[:, ['product_name',
                                 'store_url', 'price', 'store_name']]
    mt_export_df.columns = ['标题', '链接', '价格', '店铺名']
    mt_export_df.to_csv(f'E:/{today}伊婉美团销售情况.csv', index=False)


if __name__ == '__main__':
    main()
