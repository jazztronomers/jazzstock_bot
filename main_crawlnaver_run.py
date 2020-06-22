import sys
import os
import common.connector_db as db
from crawl.jazzstock_crawl_core import JazzstockCrawlCoreSlaveNaver

# 실행부, 자세한 로직은 JazzstockCrawlCoreSlaveNaver를 참조

if __name__=='__main__':

    if len(sys.argv) > 1:
        stockcode_list = sys.argv[1:]

    else:
        stockcode_list = ['079940', '093320', '035420', '060250', '131370', '023590', '239610', '035720', '036800', '119860']
        # stockcode_list = db.selectSingleColumn("SELECT STOCKCODE FROM jazzdb.T_UNIVERSE_LIST WHERE DATE = '2020-04-22' LIMIT 50")

    m = JazzstockCrawlCoreSlaveNaver(stockcode_list=stockcode_list)
    m.initialize_dataframe(cntto=0) # 마지막1거래일을 실시간으로 디버깅하겠다는 의미
    m.run()
