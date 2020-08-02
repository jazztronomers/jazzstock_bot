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
    # BIGGER 만 됨...

    '''

    컬럼을 몇개만 넣으면 적정값을 찾아주는 험수

    input:

    '%s_거래량동반돌파'%(INSTANCE_ID): {
                    'PSMAR60': ['BIGGER',0.01],
                    'VSMAR20': ['BIGGER', 0.5],
                    'TRADINGVALUE': ['BIGGER',1]
    },


    ouput:

    [
        '%s_거래량동반돌파'%(INSTANCE_ID): {
                    'PSMAR60': ['BIGGER',0.01],
                    'VSMAR20': ['BIGGER', 0.5],
                    'TRADINGVALUE': ['BIGGER',1]
        },

        '%s_거래량동반돌파'%(INSTANCE_ID): {
                    'PSMAR60': ['BIGGER',0.02],
                    'VSMAR20': ['BIGGER', 0.5],
                    'TRADINGVALUE': ['BIGGER',1]
        },
    ]

    :param cond_dict:
    :return:
    '''


    cond_name = cond_dict.keys()[0]  # 단일 컨디션만 확장해줌
    cond_key = cond_dict.values()[0].keys()

    for i in range (0,20):
        pass












COND_TEST1 = {
    '%s_BUY01' % (INSTANCE_ID): {
        'PSMAR60': ['BIGGER', 0.015],
        'VSMAR5': ['BIGGER', 3],
        'VSMAR20': ['BIGGER', 5],
        'TRADINGVALUE': ['BIGGER', 1]
    },
}



