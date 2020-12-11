import common.connector_db as db
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
from datetime import datetime

pd.set_option('display.max_columns', 10)
pd.set_option('display.expand_frame_repr', False)
pd.options.display.max_rows = 300



def _check_running_time(func):
    def new_func(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        runningtime = '%s | %s' % (func.__name__, end_time - start_time)
        # print(runningtime)
        return result
    return new_func



# FOR REAL TRADING, 최근 60개 혹은 그이상의 5분봉이 들어옴
@_check_running_time
def fillindex(ipdf):
    '''

    :param ipdf:
    :param obj:
    :return:
    '''


    opdf = ipdf.copy()
    opdf = _movingaverage_price(opdf)
    opdf = _movingaverage_volume(opdf)
    opdf = _bolinger(opdf, 20, 2)
    opdf = _stochastics(opdf, 12, 5, 5)
    # opdf = _obv(opdf)
    opdf = _rsi(opdf)
    opdf = _tradingvalue(opdf)

    # print('*********************************************')
    # print(opdf.columns)
    # print('*** DEBUG : DF LAST 5 ROW \n', opdf[['TIME','MA5','MA20','BBS','BBW','BBPD','CLOSE']].tail(1).round(3).values.tolist())
    # print('*********************************************')
    return opdf


@_check_running_time
def _tradingvalue(ipdf):
    '''
    :param ipdf:
    
    
    :return 거래대금 컬럼 추가해서 리턴
    
    '''
    
    
    opdf = ipdf.copy()
    opdf['TRADINGVALUE']=opdf['CLOSE']*opdf['VOLUME']/100000000    # 억

    return opdf




@_check_running_time
def _movingaverage_price(ipdf, n=[5,20,60], type = 0):
    '''
    :param df: META DATA + OHLC DATAFRAME, 60이평을 얻기 위해서는 최소 120줄은 들어와야 함.
    :param n: 이동평균 단위
    :param type: 0: 입력 그대로 출력하려면, nan 값 주의
                 1: 마지막 한줄만 출력하려면
    :return: row
    '''

    opdf = ipdf.copy()
    for each in n:
        opdf['PSMA'+str(each)]=opdf['CLOSE'].rolling(each).mean()

    for each in n:
        opdf['PSMAR' + str(each)] = (opdf['CLOSE'] - opdf['CLOSE'].rolling(each).mean()) / opdf['CLOSE'].rolling(each).mean()

    return opdf


@_check_running_time
def _movingaverage_volume(ipdf, n=[5,20,60], type = 0):
    '''
    :param df: META DATA + OHLC DATAFRAME, 60이평을 얻기 위해서는 최소 120줄은 들어와야 함.
    :param n: 이동평균 단위
    :param type: 0: 입력 그대로 출력하려면, nan 값 주의
                 1: 마지막 한줄만 출력하려면
    :return: row
    '''

    opdf = ipdf.copy()
    for each in n:
        opdf['VSMA'+str(each)]=opdf['VOLUME'].rolling(each).mean()
    for each in n:
        opdf['VSMAR' + str(each)] = (opdf['VOLUME'] - opdf['VOLUME'].rolling(each).mean()) / opdf['VOLUME'].rolling(each).mean()
    return opdf

@_check_running_time
def _bolinger(ipdf, n=20, m=2, ma_type='s', type = 0):
    '''

    :param ipdf:
    :param n:
    :param m:
    :param type:
    :return:
    '''

    opdf = ipdf.copy()

    # 만약에 이동평균선 데이터가 없으면 만들어준다.

    if(ma_type=='s'):

        if('PSMA'+str(n) not in opdf.columns):
            opdf = _movingaverage_price(ipdf=opdf, n=[n])

        opdf['BBU'] = opdf['PSMA'+str(n)] + m * opdf['CLOSE'].rolling(n).std()
        opdf['BBL'] = opdf['PSMA'+str(n)] - m * opdf['CLOSE'].rolling(n).std()
        opdf['BBS'] = m * opdf['CLOSE'].rolling(n).std()
        opdf['BBW'] = (opdf['BBS'] / opdf['PSMA'+str(n)]).round(3)
        opdf['BBP'] = (opdf['CLOSE'] - opdf['BBL']) / (opdf['BBU'] - opdf['BBL']).round(3)


        if('BBUD' in opdf.columns):
            opdf['BBPD'] =  (opdf['CLOSE'] - opdf['BBLD']) / (opdf['BBUD'] - opdf['BBLD']).round(3)

    elif(ma_type=='w'):

        if('PWMA'+str(n) not in opdf.columns):
            opdf = _movingaverage_weighted_price(ipdf=opdf, n=[n])

        opdf['WBBU'] = opdf['PWMA' + str(n)] + m * opdf['CLOSE'].rolling(n).std()
        opdf['WBBL'] = opdf['PWMA' + str(n)] - m * opdf['CLOSE'].rolling(n).std()
        opdf['WBBS'] = m * opdf['CLOSE'].rolling(n).std()
        opdf['WBBW'] = (opdf['WBBS'] / opdf['PWMA' + str(n)]).round(3)
        opdf['WBBP'] = (opdf['CLOSE'] - opdf['WBBL']) / (opdf['WBBU'] - opdf['WBBL']).round(3)

        if ('BBUD' in opdf.columns):
            opdf['BBPD'] = (opdf['CLOSE'] - opdf['BBLD']) / (opdf['BBUD'] - opdf['BBLD']).round(3)

    elif(ma_type=='c'):

        if('PCMA'+str(n) not in opdf.columns):
            opdf = _movingaverage_custom(ipdf=opdf, n=[n])

        opdf['CBBU'] = opdf['PCMA' + str(n)] + m * opdf['CLOSE'].rolling(n).std()
        opdf['CBBL'] = opdf['PCMA' + str(n)] - m * opdf['CLOSE'].rolling(n).std()
        opdf['CBBS'] = m * opdf['CLOSE'].rolling(n).std()
        opdf['CBBW'] = (opdf['CBBS'] / opdf['PCMA' + str(n)]).round(3)
        opdf['CBBP'] = (opdf['CLOSE'] - opdf['CBBL']) / (opdf['CBBU'] - opdf['CBBL']).round(3)

        if ('BBUD' in opdf.columns):
            opdf['BBPD'] = (opdf['CLOSE'] - opdf['BBLD']) / (opdf['BBUD'] - opdf['BBLD']).round(3)


    return opdf

@_check_running_time
def _stochastics(ipdf, n=12, m=5, t=5, type = 'row'):
    '''

    :param df: OHLC DATAFRAME 최소 120 ROWS
    :param n: n(15)일 동안의 최고가(high)와 최저가(low) 를 계산함.
    :param m: m(5)일간의 Fast%K의 이동평균 값.
    :param t: t(3)일간의 Slow%K의 이동평균 값
    :param type:
    :return:
    '''
    """
    Fast%K (K): n(15)일 동안의 최고가(high)와 최저가(low) 사이 중 현재 종가(close)의 상대적 위치를 판단하는 값
    가격이 지속적으로 상승하고 있다면 Stochastic 값은 100에 가까워 지며, 반대로 지속적으로 하락하고 있다면 Stochastic 값은 0에 가까워 지는 경향을 나타낸다.

    Slow%K (D): Fast%D라고도 하며 m(5)일간의 Fast%K의 이동평균 값
    기본값으로 5일을 설정하며 Fast%K 값을 일반화하는 역할을 한다.

    Slow%D (J): t(5)일간의 Slow%K의 이동평균 값
    기본값으로 3일을 설정하며 Slow%K 값을 일반화 하는 역할을 한다.

    Fast%K, Slow%K, Slow%D를 각각 ​K, D, J 라고하며 Stochastic을 KDJ Stochastic 지표라고 부르기도 한다.

    """

    opdf = ipdf.copy()

    # n일중 최저가 , n일중 최고가를 뽑는다
    low_min  = opdf.LOW.rolling( window = n ).min()
    high_max = opdf.HIGH.rolling( window = n ).max()

    # Fast Stochastic
    opdf['K'] = (opdf.CLOSE - low_min)/(high_max - low_min)    # K
    opdf['D'] = opdf['K'].rolling(window = m).mean()       # D

    # Slow Stochastic
    opdf['J'] = opdf['D'].rolling(window = t).mean()       # J

    return opdf
@_check_running_time
def _rsi(ipdf, period=14):
    '''
    https://wikidocs.net/3399
    키움증권이랑 값이 조금 다르게 나옴, 확인 필요함

    :param ipdf:
    :param period:
    :return:

    '''
    opdf = ipdf.copy()

    U = np.where(opdf.CLOSE.diff(1) > 0, opdf.CLOSE.diff(1), 0)
    D = np.where(opdf.CLOSE.diff(1) < 0, opdf.CLOSE.diff(1) *(-1), 0)

    AU = pd.DataFrame(U).rolling(window=period).mean()
    AD = pd.DataFrame(D).rolling(window=period).mean()
    RSI = AU.div(AD+AU) *100


    opdf['RSI'] = RSI
    return opdf

@_check_running_time
def _obv(ipdf):


    print('OBV DEBUGGING')
    print(len(ipdf))
    print('OBV DEBUGGING')


    opdf = ipdf.copy()
    opdf['OBV'] = 0
    opdf['CLOSEDIFF'] = opdf.CLOSE.diff()
    # for i, row in opdf[['DATE','CLOSEDIFF']].iterrows():
    #     if(row.CLOSEDIFF>0):
    #         opdf['OBV'].loc[i] = opdf.loc[i]['VOLUME']
    #     else:
    #         opdf['OBV'].loc[i] = -opdf.loc[i]['VOLUME']


    for j, each in enumerate(opdf[['DATE','CLOSEDIFF']].values):

        # print(j, opdf.loc[j].VOLUME)
        if each[1] > 0:
            opdf.at[j, 'OBV'] = opdf.loc[j].VOLUME
        else:
            opdf.at[j, 'OBV'] = -opdf.loc[j].VOLUME

    opdf['OBV']=opdf['OBV'].cumsum()

    # opdf= _get_quartile(opdf,['OBV'])

    return opdf

@_check_running_time
def _get_quartile(ipdf, columns=[], n=[10, 25, 75, 90]):
    opdf = ipdf.copy()

    for each in columns:

        for each_n in n:
            opdf['%s_%s'%(each, each_n)]=opdf[each].quantile(0.01*each_n)

    return opdf



@_check_running_time
def _movingaverage_weighted_price(ipdf, n=[5,20,60], type = 0):
    '''
    :param df: META DATA + OHLC DATAFRAME, 60이평을 얻기 위해서는 최소 120줄은 들어와야 함.
    :param n: 이동평균 단위
    :param type: 0: 입력 그대로 출력하려면, nan 값 주의
                 1: 마지막 한줄만 출력하려면
    :return: row
    '''


    # PANDAS NO WMA, EMA



    opdf = ipdf.sort_values('DATE',ascending=False).copy()
    # opdf = ipdf.copy()
    temp = opdf.CLOSE.values.tolist()

    colname = 'PWMA'

    for winsize in n:
        weight = [x for x in range(winsize, 0, -1)]
        wmaresult=[]
        for i in range(len(temp)):
            wmalist = []
            for idx in range(winsize):
                if(idx < len(temp[i:min(i+winsize,len(temp)-1)])):
                    wmalist.append(temp[i:min(i+winsize,len(temp)-1)][idx] * weight[idx])

            wmaresult.append(sum(wmalist)/sum(weight))

        opdf.insert(len(opdf.columns),colname+str(winsize),wmaresult)


    for each in n:
        opdf['PWMAR' + str(each)] = (opdf['CLOSE'] - opdf['PWMA'+str(each)]) / opdf['PWMA'+str(each)]


    return opdf.sort_values('DATE',ascending=True)



def _movingaverage_custom(ipdf,n=[5,20,60], type=0):
    opdf = ipdf.copy()
    opdf['CLOSEMVOLUME']= opdf['CLOSE']*opdf['VOLUME']


    for each in n:
        opdf['PCMA'+str(each)]=opdf['CLOSEMVOLUME'].rolling(each).sum()/opdf['VOLUME'].rolling(each).sum()
    for each in n:
        opdf['PCMAR' + str(each)] = (opdf['CLOSE'] - opdf['PCMA'+str(each)]) / opdf['PCMA'+str(each)]

    return opdf






def showplot(df, columns):

    df[columns].plot()
    plt.show()



if __name__ == '__main__':

    # # DAILY
    df = db.selectpd('''
    SELECT CAST(A.DATE AS CHAR) AS DATE, CNT, A.OPEN, A.HIGH, A.LOW, A.CLOSE, B.VOLUME
    FROM jazzdb.T_STOCK_OHLC_DAY A
    JOIN jazzdb.T_STOCK_SND_DAY B USING (STOCKCODE, DATE)
    JOIN jazzdb.T_DATE_INDEXED C USING (DATE)
    WHERE 1=1
    AND STOCKCODE = '032190'
    AND CNT < 10
    ORDER BY DATE ASC
    ''')
    #

    # df = db.selectpd('''
    # SELECT CAST(A.DATE AS CHAR) AS DATE, A.TIME, A.OPEN, A.HIGH, A.LOW, A.CLOSE, A.VOLUME
    # FROM jazzdb.T_STOCK_OHLC_MIN A
    # JOIN jazzdb.T_DATE_INDEXED C USING (DATE)
    # WHERE 1=1
    # AND STOCKCODE = '093320'
    # ORDER BY DATE, TIME
    # LIMIT
    # ''')

    print(df.head(10))
    print(df.tail(10))

    rt = fillindex(df)
    print(rt)


    showplot(rt, 'OBV')
