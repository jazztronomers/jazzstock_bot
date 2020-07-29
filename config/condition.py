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

COND_TEST1 = {
    '%s_BUY01' % (INSTANCE_ID): {
        'PSMAR60': ['BIGGER', 0.015],
        'VSMAR5': ['BIGGER', 3],
        'VSMAR20': ['BIGGER', 5],
        'TRADINGVALUE': ['BIGGER', 1]
    },
}



COND_SELL = {

    '%s_SELL01' % (INSTANCE_ID): {
        'PSMAR5': ['BIGGER', 0.005],
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