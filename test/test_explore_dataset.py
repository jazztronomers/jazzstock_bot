from crawl.jazzstock_object_account import JazzstockObject_Account
from crawl.jazzstock_core_simulation import JazzstockCoreSimulationCustom
import sys
import common.connector_db as db
import util.index_calculator as ic
import pandas as pd
import config.condition as cf

pd.options.display.max_rows = 1000
pd.options.display.max_columns= 500

'''

특정종목, 특정거래일의 5분봉 테이블을 지표까지 붙여서 출력하는 함수
EYE CHECKING용


'''



def date_to_index(date):
    cnt = db.selectSingleValue("SELECT CNT FROM jazzdb.T_DATE_INDEXED WHERE 1=1 AND DATE = '%s'"%(date))
    return cnt

def index_to_date(idx):
    thedate = db.selectSingleValue("SELECT CAST(DATE AS CHAR) AS DATE FROM jazzdb.T_DATE_INDEXED WHERE 1=1 AND CNT = '%s'"%(idx))
    return thedate


stockcode = '011000'
condition_dict = {'T01_TEST01':
                      {'PSMAR60': ['BIGGER',0.02],
                       'VSMAR20': ['BIGGER', 5],
                       'TRADINGVALUE': ['BIGGER',1]}}





for each_idx in range(0, -1, -1):

    the_date = index_to_date(each_idx)
    t = JazzstockCoreSimulationCustom(stockcode, condition_dict, the_date=the_date, the_date_index=each_idx, purchased=0, amount=0, hist_selled=0, hist_purchased=0)

    print(t.obj.df_ohlc_realtime_filled.columns)
    print('=' * 100)
    print(t.obj.df_ohlc_realtime_filled)
    print('=' * 100)
    # res = t.obj.simul_all_condition(condition_dict)
    # print(the_date, res)


