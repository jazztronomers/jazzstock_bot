import common.connector_db as db
import util.index_calculator as ic
import pandas as pd
from crawl.jazzstock_object_crawling import JazzstockCrawlingObject

pd.options.display.max_rows = 1000
pd.options.display.max_columns= 500

class JazzstockCoreTrading:
    def __init__(self, stockcode, to=0):
        '''

        :param stockcode:
        :param stockname:
        :param to:
        :param condition:
        '''
        self.obj = JazzstockCrawlingObject(stockcode)
        self.obj.get_daily_index(cntto=to+1)                          # to + 1, 즉 시뮬레이션 전 거래일 까지의 일봉정보를 가져옴
        self.obj.get_ohlc_min_from_db(cntto=to, window=1)             # to 거래일 까지의 5분봉을 가져옴
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

class JazzstockCoreTradingCustom(JazzstockCoreTrading):

    def __init__(self, stockcode, to=0):
        super().__init__(stockcode, to=to)

        self.BBU_UP_10, self.BBU_LOW_10=self._get_daily_bb_price(perc=10)


        #
        condition_template = {
            'day':{},
            'min':{}
        }

        # SIMPLE & 모두 AND 조건
        condition_simple = {
            'day': {'CLOSE': ('SMALLER', 7800)},
            'min': {'D': ('SMALLER',0.3)}
        }

        # SIMPLE TIME SERIES :
        #   주어진 데이터프레임에서 선후조건을 추중시켜야 하는 컨디션
        condition_timeseries = {
            'day':{'CLOSE':('SMALLER', 'MA20'),
                   'CLOSE':('BIGGER')}
            'min':{'D'}

        }

        self.condition_list = [condition_simple] # 순서중요, 순서대로 iteration 돌거

    def _operation(self, df, col, operate, value):

        if(operate=='SMALLER'):
            return df[col] < value

        elif(operate=='BIGGER'):
            return df[col] > value


    def simul_all_condition(self, condition_list):
        ret = []
        for i_cond in condition_list:
            cond_df = self.obj.df_ohlc_realtime_filled.copy()
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
        return ret

    def simulate(self):

        '''
        한바퀴 다돌림
        :return:
        '''

        ret = self.simul_all_condition(self.condition_list)
        print('*', ret[0].CLOSE.mean(), ret[0].CLOSE.count())


    def _get_daily_bb_price(self, cu):
        '''
        볼린저밴드 상하단 돌파 조건 가격을 얻는 함수
        :return: 상단 / 하단

        '''

        U = self._get_price_pierce_bbu_(self.obj.sr_daily.BBU, self.obj.sr_daily.BBL)
        D = self._get_price_pierce_bbl_(self.obj.sr_daily.BBU, self.obj.sr_daily.BBL)

        return U,D

    def _get_price_pierce_bbu_(self, BBU, BBL, cutoff= 0.1):
        '''

        :param BBU: 볼밴상단
        :param BBL: 볼밴하단
        :param cutoff: 볼밴하단 이탈율
        :return: 볼밴하단 이탈의 가격
        '''
        return cutoff*(BBU-BBL)+BBU

    def _get_price_pierce_bbl_(self, BBU, BBL, cutoff=-0.1):
        '''

        :param BBU: 볼밴상단
        :param BBL: 볼밴하단
        :param cutoff: 볼밴하단 이탈율
        :return: 볼밴하단 이탈의 가격
        '''
        return cutoff*(BBU-BBL)+BBL


if __name__=='__main__':
    t = JazzstockCoreTradingCustom('131370')
    t.simulate()
