import pandas as pd
import datetime
from settings import *

today = datetime.date.today()


def main():
    df = pd.DataFrame(list(db[MONGO_COLLECTION].find()))
    export_df = df.loc[:, ['raw_title', 'detail_url', 'view_price', 'nick']]
    export_df.columns = ['标题', '链接', '价格', '旺旺']
    export_df.to_csv(f'{today}伊婉淘宝销售情况.csv', index=False)


if __name__ == '__main__':
    main()
