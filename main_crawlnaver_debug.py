import sys
import os
import common.connector_db as db
from crawl.jazzstock_core_crawl import JazzstockCoreCrawlSlaveNaver

# 실행부, 자세한 로직은 JazzstockCrawlCoreSlaveNaver를 참조

if __name__=='__main__':

    if len(sys.argv) > 1:
        stockcode_list = sys.argv[1:]

    else:
        stockcode_list = ['079940', '093320', '035420', '060250', '131370', '023590', '239610', '035720', '036800', '119860']
        # stockcode_list = db.selectSingleColumn('SELECT STOCKCODE FROM jazzdb.T_UNIVERSE_LIST WHERE DATE = "2020-04-28" LIMIT 40')
        # stockcode_list = ['131370', '079940']


    print(stockcode_list)
    debug_date = db.selectSingleValue('SELECT CAST(DATE AS CHAR) AS DATE FROM jazzdb.T_DATE_INDEXED WHERE CNT = 0').replace('-','')


    m = JazzstockCoreCrawlSlaveNaver(stockcode_list=stockcode_list, is_debug=True, debug_date=debug_date)
    # m.initialize_dataframe(cntto=1)
    m.debug()
