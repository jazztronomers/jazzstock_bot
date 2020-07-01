import time
import requests
import warnings
import pandas as pd
import common.connector_db as db
import util.index_calculator as ic
from datetime import datetime

warnings.filterwarnings('ignore')
try:
	timedf = pd.read_csv('../config/time.csv', dtype=str)
except:
	timedf = pd.read_csv('config/time.csv', dtype=str)
	
tdic = {}
for tk, t1, t5, t15 in sorted(timedf.values.tolist()):
    tdic[str(tk).zfill(6)] = {'T1': str(t1).zfill(6), 'T5': str(t5).zfill(6), 'T15': str(t15).zfill(6)}



# =====================================================================================
# 추가구현시 FUNCTION 네이밍 참조:
# =====================================================================================
# SET_FUNC   => 객체에 뭔가를 입히는 함수, 아무것도 반환하지 않고, 객체에 입히기만 한다.
# GET_FUNC   => 객체에서 무언가를 꺼내오는 함수, 되도록 GET_FUNC 에서는 아무것도 출력하지 않고
#               CORE 부에서 메세지를 출력한다.
# CAL_FUNC   => 인풋에 대해서 뭔가를 계산하여 반환하는 함수

# _FUNC      => 객체내부에서만 사용되는 함수, 외부에서 호출할일 없는 함수는 _ 을 붙여주도록.
# =====================================================================================



class JazzstockObject:
    def __init__(self, stockcode, the_date=datetime.now().date(), the_date_index=0):

        '''

        :param stockcode:       종목코드
        :param the_date:        해당종목을 초기화할 날짜
        :param the_date_index:

        '''


        self.stockcode = stockcode
        self.stockname = db.selectSingleValue(
            'SELECT STOCKNAME FROM jazzdb.T_STOCK_CODE_MGMT WHERE STOCKCODE = "%s"' % (stockcode))
        self.the_date = the_date
        self.the_date_index = the_date_index


        # 최적화 필요 부분
        self.sr_daily = pd.Series()
        self.df_ohlc_day = pd.DataFrame()
        self.df_ohlc_min = pd.DataFrame() 
        self.df_ohlc_realtime = pd.DataFrame()
        self.df_ohlc_realtime_filled = pd.DataFrame()

        self.df_min_raw_naver = pd.DataFrame(columns=['체결시각', '체결가', '전일비', '매도', '매수', '거래량', '변동량'])
        self.OPEN = None

    def set_ohlc_day_from_db_include_index(self, window=240, cntto=0, columns=[]):
        '''

        DB에서 일봉 OHLC 정보 그리고 각종 지표를 포함하여 return 하는 함수

        :param window: 지표계산용 windows 사이즈
        :param cntto:  거래일 정보, default는 최근거래일으로 0을 준다
        :return: 일봉기준 window 범위안에 모든 지표
        '''
        query = '''

        SELECT A.DATE, A.OPEN, A.HIGH, A.LOW, A.CLOSE, B.VOLUME, 
               C.BBP, C.BBW, C.BBU, C.BBL
               , ROUND(D.K,3) AS K
               , ROUND(D.D,3) AS D
               , ROUND(D.J,3) AS J
        FROM jazzdb.T_STOCK_OHLC_DAY A
        JOIN jazzdb.T_STOCK_SND_DAY B USING (STOCKCODE, DATE)
        JOIN jazzdb.T_STOCK_BB C USING (STOCKCODE, DATE)
        JOIN jazzdb.T_STOCK_STOCH D USING (STOCKCODE, DATE)
        JOIN jazzdb.T_DATE_INDEXED E USING (DATE)
        WHERE 1=1
        AND STOCKCODE = '%s'
        AND CNT BETWEEN %s AND %s
        ORDER BY DATE ASC

        ''' % (self.stockcode, cntto, window)

        # DB에 없는 값들은 util.index_calculator.py 를 사용해서 계산
        df = db.selectpd(query)
        df = ic._get_quartile(df, ['VOLUME'])
        df = ic._rsi(df)

        if columns:
            df = df[columns]

        self.df_ohlc_day = df
        self.sr_daily=df.iloc[-1]



    def set_ohlc_min_from_db(self, window=1, cntto=0):
        '''
        DB에서 종목의 최근 분봉을 가져오는 함수
        :return:
        '''

        query = '''

        SELECT DATE, REPLACE(TIME,":","") AS TIME, OPEN, HIGH, LOW, CLOSE, VOLUME
        FROM jazzdb.T_STOCK_OHLC_MIN
        JOIN jazzdb.T_DATE_INDEXED USING (DATE)
        WHERE 1=1
        AND STOCKCODE = '%s'
        AND CNT BETWEEN %s AND %s
        ORDER BY DATE ASC, TIME ASC

        ''' % (self.stockcode, cntto, cntto+window)

        self.df_ohlc_min = db.selectpd(query)

        if(cntto==0 and window==1):
            print(" * %s(%s)의 %s일치 5분봉데이터를 DB에서 조회해왔습니다" % (self.stockname, self.stockcode, window))


    def _check_running_time(func):
        def new_func(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            runningtime = '%s | %s sec' % (func.__name__, round(end_time - start_time, 3))
            # print(runningtime)
            return result

        return new_func

    @_check_running_time
    def set_ohlc_min_from_naver(self, is_debug=False, debug_date=None):
        '''
        NAVER에서 해당종목의 당일 분단위 종가 / 거래량변동을 실행시점까지 긁어오는 함수

        :return:
        '''

        # ==========================================================================
        # 최초실행, 당일 분봉정보가 없는경우
        # 최초실행이 아니라면, 크롤링 주기가 10분이하이면 한페이지 만 긁어도 되니까 lastidx 도 1로
        if len(self.df_min_raw_naver) == 0:
            lastidx, pageidx = 1000, 1
        else:
            lastidx, pageidx = 1, 1
        # ==========================================================================

        sdate = str(datetime.now().date())
        ndate = str(datetime.now().date()).replace('-', '')

        if is_debug:
            ntime = is_debug
            ndate = debug_date

        else:

            ntime = str(datetime.now().time()).replace(':', '')

        while pageidx <= lastidx:

            # https://finance.naver.com/item/sise_time.nhn?code=079940&thistime=20200616090000&page=1
            url = "https://finance.naver.com/item/sise_time.nhn?code=%s&thistime=%s%s&page=%s" % (
                self.stockcode, ndate, ntime, pageidx)


            # print(url)

            htmls = requests.get(url).text
            ndf = pd.read_html(htmls, header=0)[0]
            ndf.columns = ['TIMESTAMP', 'CLOSE', 'FLUCT', 'HOGA_S', 'HOGA_B', 'VOLCUM', 'VOLFLUC']

            self.df_min_raw_naver = self.df_min_raw_naver.append(ndf[ndf['TIMESTAMP'].notnull()], ignore_index=True)
            self.df_min_raw_naver[['A', 'B']] = self.df_min_raw_naver.TIMESTAMP.str.split(':', expand=True).astype(int)
            self.df_min_raw_naver['TIMEKEY'] = self.df_min_raw_naver['A'].astype(str).str.pad(width=2, side='left',
                                                                                              fillchar='0') + \
                                               self.df_min_raw_naver[
                                                   'B'].astype(str).str.pad(
                                                   width=2, side='left',
                                                   fillchar='0') + '00'  # 5분봉 기준시간 COLUMN을 'HHMMSS' 형태로 변환
            self.df_min_raw_naver = self.df_min_raw_naver[
                ['TIMEKEY', 'TIMESTAMP', 'CLOSE', 'FLUCT', 'HOGA_S', 'HOGA_B', 'VOLCUM', 'VOLFLUC']]  # 불필요한 컬럼 제거

            self.df_min_raw_naver = \
                self.df_min_raw_naver.assign(rn=self.df_min_raw_naver.sort_values(['VOLCUM'], ascending=False) \
                                             .groupby(['TIMESTAMP']) \
                                             .cumcount() + 1).query('rn<2') \
                    .sort_values(['TIMESTAMP'], ascending=True)[
                    ['TIMEKEY', 'TIMESTAMP', 'CLOSE', 'FLUCT', 'HOGA_S', 'HOGA_B', 'VOLCUM', 'VOLFLUC']] \
                    .reset_index(drop=True)

            pageidx += 1
            self.timekey = self.df_min_raw_naver.TIMEKEY.max()

            # 분봉 Dataframe에 개장봉이 있으면 iterate종료
            if self.df_min_raw_naver['TIMESTAMP'].min() == '09:00':

                temp = self.df_min_raw_naver[self.df_min_raw_naver['TIMESTAMP']=='09:00']       # 시초가 세팅
                self.OPEN = int(temp.CLOSE-temp.FLUCT)
                break

    @_check_running_time
    def set_candle_five(self, is_debug=False, debug_date=False):

        rtdf = self.df_ohlc_min.copy()
        DATE = debug_date or str(datetime.now().date())
        ddf = pd.merge(self.df_min_raw_naver, timedf, on='TIMEKEY')
        ddf['DATE'] = DATE
        ddf = ddf[['DATE', 'TIMEKEY', 'T5', 'CLOSE', 'VOLFLUC']]


        for each in ddf.T5.drop_duplicates():
            temp = ddf[ddf['T5'] == each]
            OPEN = temp.CLOSE.values[0]
            HIGH = temp.CLOSE.max()
            LOW = temp.CLOSE.min()
            CLOSE = temp.CLOSE.values[-1]
            VOLUME = pd.to_numeric(temp.VOLFLUC).sum()

            rtdf.loc[len(rtdf)] = [DATE, each,
                                   int(float(OPEN)),
                                   int(float(HIGH)),
                                   int(float(LOW)),
                                   int(float(CLOSE)),
                                   int(float(VOLUME))]

        self.df_ohlc_realtime = rtdf.copy()

    @_check_running_time
    def fill_index(self):
        self.df_ohlc_realtime_filled=ic.fillindex(self.df_ohlc_realtime).tail(5)



    def get_info(self, type='DataFrame'):
        '''

        직전거래일의 정보를 싱글ROW DATAFRAME으로 반환하는 함수

        :return:
        '''
        temp = self.sr_daily
        temp['STOCKNAME'] = self.stockname
        return pd.DataFrame(temp).T[['STOCKNAME','DATE', 'CLOSE','BBP','BBW','K','D','J','VOLUME','RSI']]

    # 가장최근 분봉정보를 출력하는 함수
    def check_status(self, columns=['DATE','TIME','BBP','BBW','K','D','J'], logmode=0):
        '''
        
        :param columns 체크할 컬럼명
        :param logmode: 로깅모드, 콘솔에다 찍는 형태
        
        참고: 
            df_min_raw_naver:
            df_ohlc_realtime_filled:
        
        :return
        '''
        
        # a = 123
        # log_mode_dic= {'0':"콘솔에다 보기 좋은 형태로 프린트 - markdown / return True",
        #                '1':"콘솔에다가 dictionary로 프린트 - series 출력 / return True",
        #                '2':"dictionary를 반환                            / return dict(something)"}
                    
        # HUMAN READABLE : SINGLE LINE
        if logmode == 0:
            if(len(self.df_ohlc_realtime_filled)>1):
                print('%s'%(self.stockname.ljust(8,' ')),                          # 종목명
                    '%06s'%(self.OPEN),                                            # 시초가
                    '%s'%(self.df_min_raw_naver.tail(1).TIMEKEY.values[0]),   # 현재시각
                    '%08s'%(int(self.df_min_raw_naver.tail(1).CLOSE)),     # 현재가
                    '%04s'%(int(self.df_min_raw_naver.tail(1).FLUCT)),     # 변동
                    '|', '\t%s\t%s\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f'%tuple(self.df_ohlc_realtime_filled[columns].values[-1].tolist()) # 5분봉정보
                    )
                
        # HUMAN READABLE : MULTI LINE
        elif logmode == 1:
            print(self.stockname)
            # print('-'*80)
#             print('1분단위 체결정보:')
#             print(self.df_min_raw_naver.tail(5))
            
#             print('\n5분봉:')
#             print(self.df_ohlc_realtime_filled[columns].tail(5))
            
            '''
            OPERATION :
            
            일봉 및 5분봉의 특정 컬럼 대한 OPERATION 수행시 VALUE에 대한 요구사항
            SMALLER : args[0] (NUMERIC)
            BIGGER  : args[0] (NUMERIC)
            BETWEEN : args[0], args[1] (SMALL, BIG NUMBER)
            TRUE    : no need argument
            
            COLUMN LIST:
            
            day : OPEN, HIGH, LOW, CLOSE, K, D, J
            min : 
            VALUE LIST:
            
            '''

            condition_simple = {
                'CLOSE': ('SMALLER', self.PREV_1_LOW),
                # 'CLOSE': ('SMALLER_MINMAX_P', self.obj.PREV_1_BBU, self.obj.PREV_1_BBL, 0),
                'D': ('SMALLER', 0.2)
            }


            condition_list = [condition_simple]
            ret = self.simul_all_condition(condition_list, n=1)
            print('='*100)

            if(len(ret[0])>0):
                
                print(' * jazzstock_object.checkstatus')                
                rtdic = ret[0].to_dict('index')
                rtdic = rtdic[list(rtdic.keys())[0]]
                rtdic['STOCKNAME']=self.stockname

#                 for k in sorted(rtdic.keys()):
#                 print(k, rtdic[k])

                return rtdic
            
            pass
            
            
        elif logmode == 2:
            pass


    # ==============================================================================================
    def set_prev_day_index(self):
        '''



        :return:
        '''

        # 직전거래일 정보를 한땀한땀 현재 객체에 담아준다
        self.PREV_1_OPEN = self.sr_daily['OPEN']
        self.PREV_1_CLOSE = self.sr_daily['CLOSE']
        self.PREV_1_HIGH = self.sr_daily['HIGH']
        self.PREV_1_LOW = self.sr_daily['LOW']
        self.PREV_1_K = self.sr_daily['K']
        self.PREV_1_D = self.sr_daily['D']
        self.PREV_1_J = self.sr_daily['J']
        self.PREV_1_BBP = self.sr_daily['BBP']
        self.PREV_1_BBW = self.sr_daily['BBW']
        self.PREV_1_BBU = self.sr_daily['BBU']
        self.PREV_1_BBL = self.sr_daily['BBL']
        self.PREV_1_RSI = self.sr_daily['RSI']


        # 직전 5거래일간의 지표상 고점, 저점 등을 기록한다

        self.PREV_5_OPEN = int(self.df_ohlc_day.tail(5).head(1).OPEN)
        self.PREV_5_HIGH = self.df_ohlc_day.tail(5).HIGH.max()
        self.PREV_5_LOW  = self.df_ohlc_day.tail(5).LOW.min()
        self.PREV_5_K_HIGH  = self.df_ohlc_day.tail(5).K.max()
        self.PREV_5_K_LOW =  self.df_ohlc_day.tail(5).K.min()


        # 최근 20거래일간 볼린저밴드 관련
        # 하단보다 종가가 낮았던 일수
        # 뭐이런거


        # print(self.PREV_1_CLOSE, self.PREV_5_HIGH, self.PREV_1_K, self.PREV_5_K_HIGH, self.PREV_5_K_LOW)

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







    def simul_all_condition(self, condition_list, n=-1):
        '''

        모든 컨디션을 돌려서, 컨디션에 부합하는 DATAFRAME을
        리스트로 묶어서 반환함

        :param condition_list:
        :return: list of dataframe
        '''
        ret = []


        for i_cond in condition_list:

            if n!= -1:
                cond_df = self.df_ohlc_realtime_filled.tail(n).copy()
            else:
                cond_df = self.df_ohlc_realtime_filled.copy()
                cond_df = cond_df[cond_df['DATE']==self.the_date]
            flag=True
            for col, cond in i_cond.items():
                cond_df = cond_df[self._operation(cond_df, col, cond[0], *cond[1:])]
                if(len(cond_df)==0):
                    flag=False
                    break
            if ~flag:
                ret.append(cond_df.copy())

        #======================================================
        # DEBUGGING 영역
        #======================================================
        # print(ret)
        #======================================================
        return ret

    def _operation(self, df, col, operate, *args):
        '''



        :param df:
        :param col:
        :param operate:
        :param value:
        :return:
        '''

        if (operate == 'SMALLER'):
            return df[col] < args[0]
        elif (operate == 'BIGGER'):
            return df[col] > args[0]
        elif (operate == 'BETWEEN'):
            return (args[1] >= df[col]) & (df[col] >= args[0])

        elif (operate == 'SMALLER_P'):
            return df[col] < args[0] * (1 - args[1])
        elif (operate == 'BIGGER_P'):
            return df[col] > args[0] * (1 + args[1])

        elif (operate == 'BIGGER_MINMAX_P'):
            return df[col] > (max(args[1], args[0]) - min(args[1], args[0])) * args[2] + min(args[1], args[0])
        elif (operate == 'SMALLER_MINMAX_P'):
            print((max(args[1], args[0]) - min(args[1], args[0])) * args[2] + min(args[1], args[0]))
            return df[col] < (max(args[1], args[0]) - min(args[1], args[0])) * args[2] + min(args[1], args[0])
        elif (operate == 'TRUE'):
            return df[col] == 'True'

    def _get_daily_bb_price(self, percent):
        '''
        볼린저밴드 상하단 돌파 조건 가격을 얻는 함수
        :return: 상단 / 하단

        '''

        U = self._cal_price_pierce_bbu_(self.sr_daily.BBU, self.sr_daily.BBL, percent)
        D = self._cal_price_pierce_bbl_(self.sr_daily.BBU, self.sr_daily.BBL, percent)

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


    # 자잘한 함수들, 아직 미구현
    # def set_recent_fluct_ratio_from_market_open(self):
    #     # 시초가 대비 변동률
    #     pass
    #
    # def set_recent_fluct_ratio_from_prev_close(self):
    #     # 시초가 대비 변동률
    #     pass
    #
    # def set_recent_top_n_volume_per_stick(self, n=10, window=500):
    #     # 최근 500개 5분봉중 거래량 상위 봉 세팅
    #     pass

    # ==============================================================================================
