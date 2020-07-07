# Dataframe 에 거래대금 컬럼 추가, 거래량 지표를 사용할




# 5분봉 컬럼리스트: 
# Index(['DATE', 'TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME', 'PSMA5',
#        'PSMA20', 'PSMA60', 'PSMAR5', 'PSMAR20', 'PSMAR60', 'VSMA5', 'VSMA20',
#        'VSMA60', 'VSMAR5', 'VSMAR20', 'VSMAR60', 'BBU', 'BBL', 'BBS', 'BBW',
#        'BBP', 'K', 'D', 'J', 'OBV', 'CLOSEDIFF', 'RSI', 'TRADINGVALUE'],

TESTCOND = {
    

    'T01_HIGH_VOL_PSMAR20': {
        
                    'VSMAR20':['BIGGER', 5],       # 5분봉 거래량 / 5분봉 20이평 거래량  > 2
                    'PSMAR20':['BIGGER', 0.03],
                    'TRADINGVALUE':['BIGGER',5]    # 5분봉 거래대금 1억원 이상
    },
    
    'T02_BIG_D_VOL': {
                    'D': ['BIGGER_P' , 'K', 2],   # 5분봉 STOCHASTIC D가 K 보다 200% 높음
                    'VSMAR5':['BIGGER', 5]        # 5분봉 거래량 / 5분봉 5이평 거래량  > 2
    },
    
    'T03_HIGH_VOL': {
        
                    'VSMAR20':['BIGGER', 5],       # 5분봉 거래량 / 5분봉 20이평 거래량  > 2
                    'TRADINGVALUE':['BIGGER',1]    # 5분봉 거래대금 1억원 이상
    },
    

    
    
#     'T03_DEBUG': {
#                     'CLOSE': ['BIGGER', 10000], 
#     },

}