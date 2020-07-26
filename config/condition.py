import os
# Dataframe 에 거래대금 컬럼 추가, 거래량 지표를 사용할

# 5분봉 컬럼리스트: 
# Index(['DATE', 'TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME', 'PSMA5',
#        'PSMA20', 'PSMA60', 'PSMAR5', 'PSMAR20', 'PSMAR60', 'VSMA5', 'VSMA20',
#        'VSMA60', 'VSMAR5', 'VSMAR20', 'VSMAR60', 'BBU', 'BBL', 'BBS', 'BBW',
#        'BBP', 'K', 'D', 'J', 'OBV', 'CLOSEDIFF', 'RSI', 'TRADINGVALUE'],

if 'INSTANCE_ID' in os.environ:
	INSTANCE_ID = os.environ['INSTANCE_ID']

else:
	INSTANCE_ID = 'T01'


print(" * CONDITION INITIALIZED, instance_id: %s" %(INSTANCE_ID))
COND_PROD = {
    

    # '%s01_HV_V3o5_P2o20'%(INSTANCE_ID): {
    #                 'PSMAR20': ['BIGGER', 0.02],
    #                 'VSMAR5': ['BIGGER', 3],
    #                 'TRADINGVALUE': ['BIGGER',1]
    # },

    '%s02_HV_V5o5_P2o20'%(INSTANCE_ID): {
                    'PSMAR60': ['BIGGER',0.02],
                    'VSMAR20': ['BIGGER', 5],
                    'TRADINGVALUE': ['BIGGER',1]
    },

    # '%s_02_BIG_K_VOL'%(INSTANCE_ID): {
    #                 'K': ['BIGGER' , 0.95],
    #                 'VSMAR5':['BIGGER', 7],
    #                 'TRADINGVALUE':['BIGGER',2]
    # },
    #     'T04_DEBUG': {
    #                     'CLOSE': ['BIGGER', 10000],
    #     },

}

COND_TEST1 = {
    '%s_TEST01' % (INSTANCE_ID): {
        'PSMAR5': ['BIGGER', 0.015],
        'VSMAR20': ['BIGGER', 5],
        'TRADINGVALUE': ['BIGGER', 2]
    },
}


COND_TEST2 = {
    '%s_TEST02' % (INSTANCE_ID): {
        'PSMAR5': ['BIGGER', 0.015],
        'VSMAR5': ['BIGGER', 3],
        'VSMAR20': ['BIGGER', 5],
        'TRADINGVALUE': ['BIGGER', 2]
    },
}

COND_TEST3 = {
    '%s_TEST03' % (INSTANCE_ID): {
        'PSMAR5': ['BIGGER', 0.015],
        'VSMAR5': ['BIGGER', 3],
        'VSMAR20': ['BIGGER', 5],
        'VSMAR60': ['BIGGER', 3],
        'TRADINGVALUE': ['BIGGER', 2]
    },
}