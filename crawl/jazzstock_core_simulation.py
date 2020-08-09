import sys
import common.connector_db as db
import util.index_calculator as ic
import pandas as pd
import config.condition as cf
import argparse
from datetime import datetime
from crawl.jazzstock_object_account import JazzstockObject_Account

pd.options.display.max_rows = 1000
pd.options.display.max_columns= 500
# =====================================================================================
# 추가구현시 CLASS, FUNCTION 네이밍 참조:
# =====================================================================================
# CLASS_*    => 클래스는 Camel 케이스를 사용한다 => CamleCase
# FUNC_*     => 함수는 Snake 케이스를           => snake_case
# FUNC_SET   => 객체에 뭔가를 입히는 함수, 아무것도 반환하지 않고, 객체에 입히기만 한다.
# FUNC_GET   => 객체에서 무언가를 꺼내오는 함수, 되도록 GET_FUNC 에서는 아무것도 출력하지 않고
#               CORE 부에서 메세지를 출력한다.
# FUNC_CAL   => 인풋에 대해서 뭔가를 계산하여 반환하는 함수
# _FUNC      => 객체내부에서만 사용되는 함수, 외부에서 호출할일 없는 함수는 _ 을 붙여주도록.
# =====================================================================================


class JazzstockCoreSimulation:
    def __init__(self, stockcode, condition_buy, the_date, the_date_index, purchased=0, amount=0):
        '''

        :param stockcode:
        :param stockname:
        :param to:
        :param condition:
        '''

        self.obj = JazzstockObject_Account(stockcode, the_date, the_date_index, purchased, amount)
        self.obj.set_ohlc_day_from_db_include_index(cntto=the_date_index + 1, window=60)       # to + 1, 즉 시뮬레이션 전 거래일 까지의 일봉정보를 가져옴
        self.obj.set_ohlc_min_from_db(cntto=the_date_index, window=1)                          # to 거래일 까지의 5분봉을 가져옴
        self.obj.set_prev_day_index()

        self.obj.df_ohlc_realtime_filled = ic.fillindex(self.obj.df_ohlc_min)     # 5분봉에 지표들을 붙여줌
        self.obj.df_ohlc_realtime_filled = self.obj.df_ohlc_realtime_filled[self.obj.df_ohlc_realtime_filled.DATE==the_date]
        self.COLUMNS_DAY=['DATE', 'TIME', 'CLOSE', 'VSMAR20', 'BBP', 'BBW', 'K', 'D', 'J']
        self.COLUMNS_MIN = ['DATE', 'TIME', 'CLOSE', 'VSMAR20', 'BBP', 'BBW', 'K', 'D', 'J']

        self.condition_buy  = condition_buy

        # DEBUGGING ================================================
        # print(self.obj.df_ohlc_day.tail(2))
        # print(self.obj.df_ohlc_realtime_filled.tail(10))
        # DEBUGGING ================================================


    def run(self):
        '''
        ITR ROW BY ROW
        :return:
        '''
        pass

    def simulate(self):
        '''

        FILTERING BY CONDITION
        :return:
        '''

class JazzstockCoreSimulationCustom(JazzstockCoreSimulation):
    def __init__(self, stockcode, condition_buy, the_date, the_date_index, purchased, amount):
        super().__init__(stockcode, condition_buy, the_date, the_date_index, purchased, amount)


    def simulate(self, log_level=5):

        '''
        한바퀴 다돌림
        : param log_level   5 : END_SUMMARY
                            4 : INCLUDE
                            3 : DAILY_SUMMARY
                            3 : EACH_BUY/SELL LOG

        :return:
        '''



        purchased, selled = 0, 0
        st = datetime.now()

        for row in self.obj.df_ohlc_realtime_filled.values:
            tempdf = pd.DataFrame(data=[row], columns=self.obj.df_ohlc_realtime_filled.columns)
            res = self.obj.check_status(tempdf, condition_buy, condition_sell=None)
            if 'purchased' in res.keys():
                purchased += res['purchased']
            elif 'selled' in res.keys():
                selled += res['selled']

        close_day = self.obj.df_ohlc_realtime_filled.CLOSE.tail(1).values[0]
        return self.obj.purchased, self.obj.amount, self.obj.profit, purchased, selled, close_day


def summary(tpl):

    if tpl[1]>0:
        avg =tpl[0]/ tpl[1]
    else:
        avg = 0

    hist_purchased = tpl[3]- tpl[0]
    hist_selled = tpl[-1]

    return avg, hist_purchased, hist_selled

def date_to_index(date):
    cnt = db.selectSingleValue("SELECT CNT FROM jazzdb.T_DATE_INDEXED WHERE 1=1 AND DATE = '%s'"%(date))
    return cnt

def index_to_date(idx):
    thedate = db.selectSingleValue("SELECT DATE FROM jazzdb.T_DATE_INDEXED WHERE 1=1 AND CNT = '%s'"%(idx))
    return thedate


if __name__=='__main__':


    ## argparse는 귀찮다..

    if len(sys.argv)==2 and sys.argv[1]=='-h':

        print('''
        
        stockcode=$1
        day_from = $2
        condition_label= $3
        
        
        output:
        --------------------------
        RULE_NAME / STOCKCODE / DATE / CLOSE / 평단 / 평가손익 / 누적매수금액최대치 / 평가손익최저치
        
        ''')

    else:

        if len(sys.argv)==4:
            stocklist = [sys.argv[1]]
            day_from = int(sys.argv[2])
            day_end = 0
            condition_label = sys.argv[3]
            condition_dic_full = {'TP': cf.COND_PROD,
                                  'TA': cf.COND_TEST_A,
                                  'TB': cf.COND_TEST_B,
                                  'TC': cf.COND_TEST_C,
                                  'TD': cf.COND_TEST_D,
                                  'TE': cf.COND_TEST_E}

            condition_dic_selected = condition_dic_full[condition_label]

            print(' * FROM COMMAND LINE, STOCKCODE: %s, FROM DAY_IDX: %s, CONDITION: %s' %(stocklist[0], day_from, list(condition_dic_selected.keys())[0]))
        else:
            print(' * FROM PYCHARM')
            query = '''
            SELECT STOCKCODE
            FROM
            (
                SELECT STOCKCODE, 
                        CASE WHEN RN <= 120 THEN "A"
                             WHEN RN <= 240 THEN "B"
                             WHEN RN <= 360 THEN "C"
                             WHEN RN <= 480 THEN "D"
                             WHEN RN <= 600 THEN "E"
                             WHEN RN <= 720 THEN "F"
                             WHEN RN <= 840 THEN "G"
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
            AND GRP IN ('A')
            LIMIT 10
            '''
            # sl = db.selectSingleColumn(query)
            stocklist = ['093320']
            day_from = 30
            day_end = 0
            condition_dic_selected=cf.COND_PROD




        for j, cond in enumerate(stocklist):
            condition_buy = condition_dic_selected
            stock_dic = {}
            print('* -----------------------------------------------')
            for stockcode in stocklist:

                PURCHASED_HIGH = 0 # 가장 많이 샀을때
                LOSS_HIGH = 0      # 평가금액 기준 가장 많이 잃었을때



                for each_idx in range(day_from, day_end-1, -1):
                    the_date = index_to_date(each_idx)
                    if stockcode not in stock_dic.keys():
                        stock_dic[stockcode]= (0, 0, 0, 0 ,0)
                    t = JazzstockCoreSimulationCustom(stockcode, condition_buy, the_date=the_date, the_date_index=each_idx, purchased=stock_dic[stockcode][0], amount=stock_dic[stockcode][1])
                    try:

                        # print(' * START %s / %s ' %(stockcode, the_date))
                        hold_purchased, amount, profit, purchased, selled, close_day, = t.simulate()
                        temp = list(stock_dic[stockcode])
                        temp[0] = int(hold_purchased)
                        temp[1] = int(amount)
                        temp[2] = temp[2] + int(profit)
                        temp[3] = temp[3] + purchased
                        temp[4] = temp[4] + selled
                        stock_dic[stockcode] = tuple(temp)

                        PURCHASED_HOLD, AMOUNT_HOLD, PROFIT, _, _ = stock_dic[stockcode]
                        AVERAGE_HOLD, PURCHASED_CUM, SELL_CUM = summary(stock_dic[stockcode])

                        if AVERAGE_HOLD != 0:
                            PROFIT_RATIO = round(( close_day - AVERAGE_HOLD ) / close_day,3)*100
                        else:
                            PROFIT_RATIO = 0

                        PURCHASED_HIGH = max(PURCHASED_HIGH, PURCHASED_HOLD)
                        LOSS_HIGH = min(AMOUNT_HOLD * close_day - PURCHASED_HOLD, LOSS_HIGH)

                        print('* DAILY_%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%.3f\t%s\t%s' % (list(condition_buy.keys())[0],
                                                                         stockcode,
                                                                         the_date,
                                                                         PURCHASED_HOLD,                            # 보유금액
                                                                         AMOUNT_HOLD * close_day,                   # 평가금액
                                                                         AMOUNT_HOLD * close_day - PURCHASED_HOLD,  # 기대수익
                                                                         PROFIT,
                                                                         PURCHASED_CUM,
                                                                         SELL_CUM,
                                                                         0 if PURCHASED_CUM == 0 else PROFIT/PURCHASED_CUM*100,
                                                                         PURCHASED_HIGH,
                                                                         LOSS_HIGH))





                    except Exception as e:
                        print('* ERROR %s, %s '%(e, stockcode))
                print('* WHOLE_%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%.3f\t%s\t%s' % (list(condition_buy.keys())[0],
                                                                         stockcode,
                                                                         the_date,
                                                                         PURCHASED_HOLD,                            # 보유금액
                                                                         AMOUNT_HOLD * close_day,                   # 평가금액
                                                                         AMOUNT_HOLD * close_day - PURCHASED_HOLD,  # 기대수익
                                                                         PROFIT,
                                                                         PURCHASED_CUM,
                                                                         SELL_CUM,
                                                                         0 if PURCHASED_CUM == 0 else PROFIT/PURCHASED_CUM*100,
                                                                         PURCHASED_HIGH,
                                                                         LOSS_HIGH))
