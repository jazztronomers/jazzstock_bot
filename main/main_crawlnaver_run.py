import sys
import os
import common.connector_db as db
import time
from datetime import datetime
from crawl.jazzstock_core_realtime import JazzstockCoreRealtimeNaver

# 실행부, 자세한 로직은 JazzstockCrawlCoreSlaveNaver를 참조

if __name__=='__main__':

    if len(sys.argv) > 1:
        stockcode_list = sys.argv[1:]

    else:
        # stockcode_list = ['079940', '093320', '035420', '060250', '131370', '023590', '239610', '035720', '036800', '119860']
        # stockcode_list = ['079940', '093320']
        stockcode_list = db.selectSingleColumn("SELECT STOCKCODE "
                                                "FROM jazzdb.T_STOCK_SND_ANALYSIS_RESULT_TEMP "
                                                "JOIN jazzdb.T_DATE_INDEXED USING (DATE) "
                                                "JOIN jazzdb.T_STOCK_MC USING(STOCKCODE, DATE) "
                                                "WHERE 1=1 "
                                                "AND CNT=0 "
                                                "AND MC > 1 "
                                                "ORDER BY YG5 "
                                                "LIMIT 150 ")

    print('LEN : %s'%(len(stockcode_list)))
    time.sleep(4)
    the_date = datetime.now().date()
    the_date_index = 0

    m = JazzstockCoreRealtimeNaver(stockcode_list = stockcode_list, the_date=the_date, the_date_index=the_date_index)
    m.run()
