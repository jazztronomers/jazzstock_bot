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


    '%s_거래량동반돌파'%(INSTANCE_ID): {
                    'PSMAR60': ['BIGGER',0.02],
                    'VSMAR20': ['BIGGER', 5],
                    'TRADINGVALUE': ['BIGGER',1]
    },


}


COND_TEMPLATE = {


    '%s_거래량동반돌파'%(INSTANCE_ID): {
                    'PSMAR60': ['BIGGER',0.01],
                    'VSMAR20': ['BIGGER', 0.5],
                    'TRADINGVALUE': ['BIGGER',1]
    },


}


COND_TEST_C= {
    'TEST_DEBUG': {
        'VSMAR5': ['BIGGER', 1],
        'VSMAR20': ['BIGGER', 8],
        'PSMAR60': ['BIGGER', 0.015],
        'VOLUME': ['BIGGER', '20D_85QTILE_VOL'],
        'CLOSE': ['SMALLER_P', '05D_HIGH', 0.05],
        'TRADINGVALUE': ['BIGGER', 1]
    },
}

COND_TEST_A= {
    'TEST_DEBUG': {
        'VSMAR5': ['BIGGER', 2],
        'VSMAR20': ['BIGGER', 8],
        'PSMAR60': ['BIGGER', 0.015],
        'VOLUME': ['BIGGER', '20D_85QTILE_VOL'],
        'CLOSE': ['SMALLER_P', '05D_HIGH', 0.05],
        'TRADINGVALUE': ['BIGGER', 1]
    },
}

COND_TEST_B= {
    'TEST_DEBUG': {
        'VSMAR5': ['BIGGER', 1],
        'VSMAR20': ['BIGGER', 10],
        'PSMAR60': ['BIGGER', 0.015],
        'VOLUME': ['BIGGER', '20D_85QTILE_VOL'],
        'CLOSE': ['SMALLER_P', '05D_HIGH', 0.05],
        'TRADINGVALUE': ['BIGGER', 1]
    },
}

COND_TEST_D= {
    'TEST_DEBUG': {
        'VSMAR5': ['BIGGER', 1],
        'VSMAR20': ['BIGGER', 8],
        'PSMAR60': ['BIGGER', 0.017],
        'VOLUME': ['BIGGER', '20D_85QTILE_VOL'],
        'CLOSE': ['SMALLER_P', '05D_HIGH', 0.05],
        'TRADINGVALUE': ['BIGGER', 1]
    },
}

COND_TEST_E= {
    'TEST_DEBUG': {
        'VSMAR5': ['BIGGER', 1],
        'VSMAR20': ['BIGGER', 8],
        'PSMAR60': ['BIGGER', 0.015],
        'VOLUME': ['BIGGER', '20D_85QTILE_VOL'],
        'CLOSE': ['SMALLER_P', '05D_HIGH', 0.06],
        'TRADINGVALUE': ['BIGGER', 1]
    },
}

condition_dict = {

    'TA': COND_TEST_A,
    'TB': COND_TEST_B,
    'TC': COND_TEST_C,
    'TD': COND_TEST_D,
    'TE': COND_TEST_E,
    'TP': COND_PROD,
}