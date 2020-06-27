import common.connector_db as db
import util.index_calculator as ic
import pandas as pd
from crawl.jazzstock_object_crawling import JazzstockCrawlingObject

pd.options.display.max_rows = 1000
pd.options.display.max_columns= 500

obj = JazzstockCrawlingObject('131370','알서포트')
obj.get_daily_index(cntto=1)                    # -1 거래일 까지의 일봉정보를 가져옴
obj.set_ohlc_min_from_db(cntto=0)               # -0 거래일 까지의 5분봉을 가져옴
obj.df_ohlc_min = ic.fillindex(obj.df_ohlc_min) # 5분봉에 지표들을 붙여줌

print(obj.df_ohlc_min.columns)

SHOW_COLUMNS=['DATE', 'TIME', 'CLOSE', 'VSMAR20', 'BBP', 'BBW', 'K', 'D', 'J']

print(obj.df_ohlc_min[obj.df_ohlc_min['VSMAR20']>1])


# AUTOML에서 쓰던 함수들 다 가져와서 util을 만들자
# _equal()
# _bigger()
# _smaller()



