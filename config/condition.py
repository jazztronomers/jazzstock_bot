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



def condition_generator_bigger(cond_dict):
    '''

    언제 만들꺼 ??
    :param cond_dict:
    :return:
    '''


COND_TEST_A = {
    '%sAAA'%(INSTANCE_ID): {
                    'PSMAR60': ['BIGGER',0.02],
                    'VSMAR20': ['BIGGER', 8],
                    'TRADINGVALUE': ['BIGGER',1]
    },
}

COND_TEST_B= {
    '%sDDD'%(INSTANCE_ID): {
                    'PSMAR60': ['BIGGER',0.02],
                    'VSMAR20': ['BIGGER', 5],
                    'VSMAR5': ['BIGGER', 2.5],
                    'TRADINGVALUE': ['BIGGER',1]
    },
}
COND_TEST_C= {
    'TEST_DEBUG': {
        'VSMAR5': ['BIGGER', 1],
        'VSMAR20': ['BIGGER', 1.5],
        'VSMAR60': ['BIGGER', 3],
        'PSMAR60': ['BIGGER', 0.015],
        'VOLUME': ['BIGGER', '20D_85QTILE_VOL'],
        'TRADINGVALUE': ['BIGGER', 1]
    },
}
