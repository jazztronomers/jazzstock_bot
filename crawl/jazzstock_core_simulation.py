import common.connector_db as db
import util.index_calculator as ic
import pandas as pd
from crawl.jazzstock_object import JazzstockObject

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
    def __init__(self, stockcode, the_date, the_date_index):
        '''

        :param stockcode:
        :param stockname:
        :param to:
        :param condition:
        '''
        self.obj = JazzstockObject(stockcode, the_date, the_date_index)


        self.obj.set_ohlc_day_from_db_include_index(cntto=the_date_index + 1, window=60)       # to + 1, 즉 시뮬레이션 전 거래일 까지의 일봉정보를 가져옴
        self.obj.set_ohlc_min_from_db(cntto=the_date_index, window=1)             # to 거래일 까지의 5분봉을 가져옴
        self.obj.set_prev_day_index()

        self.obj.df_ohlc_realtime_filled = ic.fillindex(self.obj.df_ohlc_min)     # 5분봉에 지표들을 붙여줌
        self.COLUMNS_DAY=['DATE', 'TIME', 'CLOSE', 'VSMAR20', 'BBP', 'BBW', 'K', 'D', 'J']
        self.COLUMNS_MIN = ['DATE', 'TIME', 'CLOSE', 'VSMAR20', 'BBP', 'BBW', 'K', 'D', 'J']


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
    def __init__(self, stockcode, the_date, the_date_index):
        super().__init__(stockcode, the_date, the_date_index)



        # ===================================================================
        # Condition 만 구현해서 타 객체에서 불러오도록 수정.
        # 밑에는 일단 간단한 condition

        # SIMPLE & 모두 AND 조건, 위에서 부터 연산을 진행하고, 위에서 False 가 반환되면 밑은 계산하지 않음.




        # 일봉기준으로 전일 저가보다 낮으면서, 5분봉기준 STOCHASTIC D 가 0.2 이하인 종목을 추출하는 조건
        condition_simple = {
            'CLOSE': ('SMALLER_P', self.obj.PREV_1_LOW, 0.01),
            'CLOSE': ('SMALLER_MINMAX_P', self.obj.PREV_1_BBU, self.obj.PREV_1_BBL, 0),
            'D': ('SMALLER',0.5)
        }
        # ===================================================================

        self.condition_list = [condition_simple] # 순서중요, 순서대로 iteration 돌거




    def simulate(self):

        '''
        한바퀴 다돌림
        :return:
        '''

        ret = self.obj.simul_all_condition(self.condition_list)

        if(ret):
            print('*', self.obj.the_date, ret[0].CLOSE.mean(), ret[0].CLOSE.count())
            return ret[0].CLOSE.mean(), int(ret[0].CLOSE.count())
        else:
            return False












def date_to_index(date):

    cnt = db.selectSingleValue("SELECT CNT FROM jazzdb.T_DATE_INDEXED WHERE 1=1 AND DATE = '%s'"%(date))
    return cnt

def index_to_date(idx):


    thedate = db.selectSingleValue("SELECT DATE FROM jazzdb.T_DATE_INDEXED WHERE 1=1 AND CNT = '%s'"%(idx))
    return thedate

if __name__=='__main__':


    # the_date = '2020-06-26'
    # the_date_index = date_to_index(the_date)
    # t = JazzstockCoreSimulationCustom('131370', the_date=the_date, the_date_index=the_date_index)
    # t.simulate()

    s, c = 0, 0
    for each_idx in range (34,0,-1):

        the_date = index_to_date(each_idx)
        t = JazzstockCoreSimulationCustom('036800', the_date=the_date, the_date_index=each_idx)
        rt = t.simulate()

        if rt and rt[1] > 0:
            s = s+(rt[0]*rt[1])
            c = c+rt[1]

    print(s/c)