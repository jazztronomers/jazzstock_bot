import common.connector_db as db
import util.index_calculator as ic
import pandas as pd
from crawl.jazzstock_object_crawling import JazzstockCrawlingObject

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


class JazzstockCoreTrading:
    def __init__(self, stockcode, to=0):
        '''

        :param stockcode:
        :param stockname:
        :param to:
        :param condition:
        '''
        self.obj = JazzstockCrawlingObject(stockcode)
        self.obj.set_ohlc_day_from_db_include_index(cntto=to + 1)       # to + 1, 즉 시뮬레이션 전 거래일 까지의 일봉정보를 가져옴
        self.obj.set_ohlc_min_from_db(cntto=to, window=1)             # to 거래일 까지의 5분봉을 가져옴
        self.obj.df_ohlc_realtime_filled = ic.fillindex(self.obj.df_ohlc_min)     # 5분봉에 지표들을 붙여줌


        self.thedate =db.selectSingleValue('SELECT DATE FROM jazzdb.T_DATE_INDEXED WHERE CNT = %s'%(to))

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

class JazzstockCoreTradingCustom(JazzstockCoreTrading):
    def __init__(self, stockcode, to=0):
        super().__init__(stockcode, to=to)

        self.set_prev_day_index()

        # ===================================================================
        # Condition 만 구현해서 타 객체에서 불러오도록 수정.
        # 밑에는 일단 간단한 condition

        # SIMPLE & 모두 AND 조건, 위에서 부터 연산을 진행하고, 위에서 False 가 반환되면 밑은 계산하지 않음.
        condition_simple = {
            'day': {
                'CLOSE': ('SMALLER', self.PREV_1_LOW)
            },
            'min': {
                'D': ('SMALLER',0.3)
            }
        }
        # ===================================================================

        self.condition_list = [condition_simple] # 순서중요, 순서대로 iteration 돌거


    def set_prev_day_index(self):
        '''



        :return:
        '''

        # 직전거래일 정보를 한땀한땀 현재 객체에 담아준다
        self.PREV_1_OPEN = self.obj.sr_daily['OPEN']
        self.PREV_1_CLOSE = self.obj.sr_daily['CLOSE']
        self.PREV_1_HIGH = self.obj.sr_daily['HIGH']
        self.PREV_1_LOW = self.obj.sr_daily['LOW']
        self.PREV_1_K = self.obj.sr_daily['K']
        self.PREV_1_D = self.obj.sr_daily['D']
        self.PREV_1_J = self.obj.sr_daily['J']
        self.PREV_1_BBP = self.obj.sr_daily['BBP']
        self.PREV_1_BBW = self.obj.sr_daily['BBW']
        self.PREV_1_RSI = self.obj.sr_daily['RSI']


        # ======================================================
        # 직전 N일 동안 일봉지표상 특이한 사항을 현재 객체에 담아준다
        # example:
        #       골든크로스가 몇 거래일전에 발생했다던가
        #       현재 골든크로스 구간이라던가
        #       일봉볼린저밴드가 어쩌고 저쩌고, 로직구현이 좀 복잡해서 보류:
        # ======================================================


        # 적전거래일 일봉기준 볼린저밴드 상하단 돌파 가격선을 세팅함
        # percent는 몇프로 돌파하는지에 대한 threshold값을 얻기 위함
        self.BBU_UP_10, self.BBU_LOW_10 = self._get_daily_bb_price(percent=0.1)
        self.BBU_UP_20, self.BBU_LOW_20 = self._get_daily_bb_price(percent=0.2)

        print(self.obj.sr_daily)

    def simulate(self):

        '''
        한바퀴 다돌림
        :return:
        '''

        ret = self.simul_all_condition(self.condition_list)
        print('*', ret[0].CLOSE.mean(), ret[0].CLOSE.count())

    def _operation(self, df, col, operate, value):
        '''



        :param df:
        :param col:
        :param operate:
        :param value:
        :return:
        '''

        if(operate=='SMALLER'):
            return df[col] < value
        elif(operate=='BIGGER'):
            return df[col] > value


    def simul_all_condition(self, condition_list):
        '''

        모든 컨디션을 돌려서, 컨디션에 부합하는 DATAFRAME을
        리스트로 묶어서 반환함

        :param condition_list:
        :return: list of dataframe
        '''
        ret = []


        for i_cond in condition_list:
            cond_df = self.obj.df_ohlc_realtime_filled.copy()
            cond_df = cond_df[cond_df['DATE']==self.thedate]
            flag=True
            for col, cond in i_cond['day'].items():
                cond_df = cond_df[self._operation(cond_df, col, cond[0], cond[1])]
                if(len(cond_df)==0):
                    flag=False
                    break
            if not flag:
                break
            for col, cond in i_cond['min'].items():
                cond_df = cond_df[self._operation(cond_df, col, cond[0], cond[1])]
                if(len(cond_df)==0):
                    flag = False
                    break
            if ~flag:
                ret.append(cond_df.copy())

        #======================================================
        # DEBUGGING 영역
        #======================================================
        print(ret)
        #======================================================
        return ret




    def _get_daily_bb_price(self, percent):
        '''
        볼린저밴드 상하단 돌파 조건 가격을 얻는 함수
        :return: 상단 / 하단

        '''

        U = self._cal_price_pierce_bbu_(self.obj.sr_daily.BBU, self.obj.sr_daily.BBL, percent)
        D = self._cal_price_pierce_bbl_(self.obj.sr_daily.BBU, self.obj.sr_daily.BBL, percent)

        return U,D

    def _cal_price_pierce_bbu_(self, BBU, BBL, percent):
        '''

        :param BBU: 볼밴상단
        :param BBL: 볼밴하단
        :param cutoff: 볼밴하단 이탈율
        :return: 볼밴하단 이탈의 가격
        '''
        return percent*(BBU-BBL)+BBU

    def _cal_price_pierce_bbl_(self, BBU, BBL, percent):
        '''

        :param BBU: 볼밴상단
        :param BBL: 볼밴하단
        :param cutoff: 볼밴하단 이탈율
        :return: 볼밴하단 이탈의 가격
        '''
        return percent*(BBU-BBL)+BBL




def date_to_index(date):

    cnt = db.selectSingleValue("SELECT CNT FROM jazzdb.T_DATE_INDEXED WHERE 1=1 AND DATE = '%s'"%(date))
    return cnt

if __name__=='__main__':

    date = date_to_index('2020-06-26')
    t = JazzstockCoreTradingCustom('131370', to=date)
    t.simulate()
