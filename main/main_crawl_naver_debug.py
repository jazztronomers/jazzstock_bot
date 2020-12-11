import sys
import common.connector_db as db
import config.condition as cd
from object.jazzstock_core_realtime import JazzstockCoreRealtimeNaver

# 실행부, 자세한 로직은 JazzstockCrawlCoreSlaveNaver를 참조

if __name__=='__main__':

    if len(sys.argv) > 1:
        stockcode_list = sys.argv[1:]

    else:
        stockcode_list = ['079940']

    cond = cd.COND_PROD

    # ['DATE', 'TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME', 'PSMA5', 'PSMA20', 'PSMA60', 'PSMAR5', 'PSMAR20',
    #  'PSMAR60', 'VSMA5', 'VSMA20', 'VSMA60', 'VSMAR5', 'VSMAR20', 'VSMAR60', 'BBU', 'BBL', 'BBS', 'BBW', 'BBP', 'K',
    #  'D', 'J', 'OBV', 'CLOSEDIFF', 'RSI', 'TRADINGVALUE']

    # ['01D_DATE', '01D_OPEN', '01D_HIGH', '01D_LOW', '01D_CLOSE', '01D_VOLUME', '01D_BBP', '01D_BBW', '01D_BBU',
    #  '01D_BBL', '01D_K', '01D_D', '01D_J', '01D_I1', '01D_I5', '01D_I20', '01D_I60', '01D_F1', '01D_F5', '01D_F20',
    #  '01D_F60', '01D_S1', '01D_S5', '01D_S20', '01D_S60', '01D_YG1', '01D_YG5', '01D_YG20', '01D_YG60', '01D_T1',
    #  '01D_T5', '01D_T20', '01D_T60', '01D_FN1', '01D_FN5', '01D_FN20', '01D_FN60', '01D_RSI', '05D_HIGH', '05D_LOW',
    #  '60D_HIGH', '60D_LOW'
    #  '20D_TOP20_MEAN_VOL', '20D_TOP20_MEAN_FLUCT', '20D_TOP20_MEAN_CLOSE']

    cond = {


    'TEST_DEBUG': {

                    'VSMAR5': ['BIGGER', 1],
                    'VSMAR20': ['BIGGER', 1.5],
                    'VSMAR60': ['BIGGER', 3],
                    'PSMAR60': ['BIGGER',0.015],
                    'VOLUME': ['BIGGER', '20D_85QTILE_VOL'],
                    'TRADINGVALUE': ['BIGGER',1]
    },


}

    the_date_index = 0
    the_date = db.selectSingleValue('SELECT CAST(DATE AS CHAR) AS DATE FROM jazzdb.T_DATE_INDEXED WHERE CNT = %s'%(the_date_index)).replace('-','')
    m = JazzstockCoreRealtimeNaver(stockcode_list = stockcode_list,
                                   the_date=the_date,
                                   the_date_index=the_date_index,
                                   condition_dict = cond)
    m.debug()
