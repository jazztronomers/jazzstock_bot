import time
import requests
import warnings
import pandas as pd
import common.connector_db as db
import util.index_calculator as ic
from datetime import datetime

warnings.filterwarnings('ignore')
timedf = pd.read_csv('config/time.csv', dtype=str)

tdic = {}
for tk, t1, t5, t15 in sorted(timedf.values.tolist()):
    tdic[str(tk).zfill(6)] = {'T1': str(t1).zfill(6), 'T5': str(t5).zfill(6), 'T15': str(t15).zfill(6)}


class JazzstockCrawlingObject:
    def __init__(self, stockcode, stockname, use_db=False, debug=False):

        # DEBUGGING 여부 판단
        self.debug = debug 
        self.use_db = use_db
        self.stockcode = stockcode
        self.stockname = db.selectSingleValue(
            'SELECT STOCKNAME FROM jazzdb.T_STOCK_CODE_MGMT WHERE STOCKCODE = "%s"' % (stockcode))

        # 최적화 필요 부분
        self.sr_daily = pd.Series()
        self.df_ohlc_min = pd.DataFrame() 
        self.df_ohlc_realtime = pd.DataFrame()
        self.df_ohlc_realtime_filled = pd.DataFrame()

        self.df_min_raw_naver = pd.DataFrame(columns=['체결시각', '체결가', '전일비', '매도', '매수', '거래량', '변동량'])


        self.OPEN = None


    def get_daily_index(self, window=240, cntto=0):

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
        self.sr_daily = df.iloc[-1]






    def get_ohlc_min_from_db(self, window=120, cntto=0):
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
        AND CNT BETWEEN %s AND 10
        ORDER BY DATE ASC, TIME ASC

        ''' % (self.stockcode, cntto)

        self.df_ohlc_min = db.selectpd(query)

        print(" * %s(%s)의 %s일치 5분봉데이터를 DB에서 조회해왔습니다" % (self.stockname, self.stockcode, window))

    def check_running_time(func):
        def new_func(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()

            runningtime = '%s | %s' % (func.__name__, end_time - start_time)
            # print(runningtime)
            return runningtime

        return new_func

    @check_running_time
    def get_ohlc_min_from_naver(self, is_debug=False, debug_date=None):
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

    @check_running_time
    def get_candle_five(self, is_debug=False, debug_date=False):

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


    @check_running_time
    def fill_index(self):
        self.df_ohlc_realtime_filled=ic.fillindex(self.df_ohlc_realtime).tail(5)

    # 직전거래일 정보를 리턴하는 함수
    def get_prev(self):

        temp = self.sr_daily
        temp['STOCKNAME']=self.stockname
        return pd.DataFrame(temp).T[['STOCKNAME','CLOSE','BBP','BBW','K','D','J','VOLUME', 'VOLUME_25', 'VOLUME_75','RSI']]

    # 가장최근 분봉정보를 출력하는 함수
    def check_status(self, min_1_line=0, min_5_line=1, columns=['DATE','TIME','BBP','BBW','K','D','J']):

#         print('*** %s (%s) -- %s' % (self.stockname, self.stockcode, datetime.now().time()))
#         print(self.df_min_raw_naver.tail(3))
#         print(self.df_ohlc_realtime.tail(3))
#         print(self.df_ohlc_realtime_filled)

        if(len(self.df_ohlc_realtime_filled)>1):
            print('%s'%(self.stockname.ljust(8,' ')),                          # 종목명
                '%06s'%(self.OPEN),                                            # 시초가
                '%s'%(self.df_min_raw_naver.tail(1).TIMEKEY.values[0]),   # 현재시각
                '%08s'%(int(self.df_min_raw_naver.tail(1).CLOSE)),     # 현재가
                '%04s'%(int(self.df_min_raw_naver.tail(1).FLUCT)),     # 변동
                '|', '\t%s\t%s\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f'%tuple(self.df_ohlc_realtime_filled[columns].values[-1].tolist()) # 5분봉정보
                )



    # ==============================================================================================
    # 자잘한 함수들, 아직 미구현
    def set_recent_fluct_ratio_from_market_open(self):
        # 시초가 대비 변동률
        pass

    def set_recent_fluct_ratio_from_prev_close(self):
        # 시초가 대비 변동률
        pass

    def set_recent_top_n_volume_per_stick(self, n=10, window=500):
        # 최근 500개 5분봉중 거래량 상위 봉 세팅
        pass

    # ==============================================================================================
