import sys
import common.connector_db as db
from datetime import datetime
from object.jazzstock_core_realtime import JazzstockCoreRealtimeNaver

if __name__=='__main__':

    if len(sys.argv) == 2 and sys.argv[1] in list('ABCDEFGHIJKL'):
        instance_id = sys.argv[1]
        query = '''
        SELECT STOCKCODE
        FROM
        (
            SELECT STOCKCODE, 
                    CASE WHEN RN <= 200 THEN "A"
                         WHEN RN <= 400 THEN "B"
                         WHEN RN <= 600 THEN "C"
                         WHEN RN <= 800 THEN "D"
                         WHEN RN <= 1000 THEN "E"
                         WHEN RN <= 1200 THEN "F"
                         WHEN RN <= 1400 THEN "G"
                         ELSE "H" END AS GRP
            FROM
            (
                SELECT STOCKCODE, 
                    ROW_NUMBER() OVER (PARTITION BY DATE ORDER BY I5+F5 DESC) AS RN
                FROM jazzdb.T_STOCK_SND_ANALYSIS_RESULT_TEMP
                JOIN jazzdb.T_DATE_INDEXED USING (DATE)
                JOIN jazzdb.T_STOCK_MC USING (STOCKCODE, DATE)
                WHERE 1=1
                AND CNT = 0
                AND MC > 1          # 1300종목
            ) A
        ) B        
        WHERE 1=1
        AND GRP = "%s"
        ''' % (instance_id)
        stockcode_list = db.selectSingleColumn(query)
        print(' * INSTANCE_ID: %s'%(instance_id))

    elif len(sys.argv) > 1:
        stockcode_list = sys.argv[1:]
    else:
        stockcode_list = ['058470', '115180']

    print(' * LEN: %s'%(len(stockcode_list)))
    the_date = datetime.now().date()
    the_date_index = 0
    m = JazzstockCoreRealtimeNaver(stockcode_list = stockcode_list, the_date=the_date, the_date_index=the_date_index)
    m.run()
