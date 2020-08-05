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
    '%sA01'%(INSTANCE_ID): {
                    'PSMAR60': ['BIGGER', 0.02],
                    'VSMAR20': ['BIGGER', 5],
                    'TRADINGVALUE': ['BIGGER',1]
    },
}

COND_TEST2 = {
    '%sA02'%(INSTANCE_ID): {
                    'PSMAR60': ['BIGGER',0.02],
                    'VSMAR20': ['BIGGER', 6],
                    'TRADINGVALUE': ['BIGGER',1]
    },
}

COND_TEST3 = {
    '%sA03'%(INSTANCE_ID): {
                    'PSMAR60': ['BIGGER',0.02],
                    'VSMAR20': ['BIGGER', 7],
                    'TRADINGVALUE': ['BIGGER',1]
    },
}

COND_TEST4 = {
    '%sA04'%(INSTANCE_ID): {
                    'PSMAR60': ['BIGGER',0.02],
                    'VSMAR20': ['BIGGER', 8],
                    'TRADINGVALUE': ['BIGGER',1]
    },
}

COND_TEST5 = {
    '%sA05'%(INSTANCE_ID): {
                    'PSMAR60': ['BIGGER',0.02],
                    'VSMAR20': ['BIGGER', 9],
                    'TRADINGVALUE': ['BIGGER',1]
    },
}

COND_TEST6 = {
    '%sB01'%(INSTANCE_ID): {
                    'PSMAR60': ['BIGGER',0.02],
                    'VSMAR20': ['BIGGER', 10],
                    'TRADINGVALUE': ['BIGGER',1]
    },
}

COND_TEST7 = {
    '%s01'%(INSTANCE_ID): {
                    'PSMAR60': ['BIGGER',0.02],
                    'VSMAR20': ['BIGGER', 5],
                    'VSMAR5':['BIGGER',1],
                    'TRADINGVALUE': ['BIGGER',1]
    },
}

COND_TEST8 = {
    '%s01'%(INSTANCE_ID): {
                    'PSMAR60': ['BIGGER',0.02],
                    'VSMAR20': ['BIGGER', 5],
                    'VSMAR5': ['BIGGER', 1.5],
                    'TRADINGVALUE': ['BIGGER',1]
    },
}

COND_TEST9 = {
    '%s01'%(INSTANCE_ID): {
                    'PSMAR60': ['BIGGER',0.02],
                    'VSMAR20': ['BIGGER', 5],
                    'VSMAR5': ['BIGGER', 2],
                    'TRADINGVALUE': ['BIGGER',1]
    },
}

COND_TEST10 = {
    '%s01'%(INSTANCE_ID): {
                    'PSMAR60': ['BIGGER',0.02],
                    'VSMAR20': ['BIGGER', 5],
                    'VSMAR5': ['BIGGER', 2.5],
                    'TRADINGVALUE': ['BIGGER',1]
    },
}

COND_TEST11 = {
    '%s01'%(INSTANCE_ID): {
                    'PSMAR60': ['BIGGER',0.02],
                    'VSMAR20': ['BIGGER', 5],
                    'TRADINGVALUE': ['BIGGER',1]
    },
}

COND_TEST12 = {
    '%s01'%(INSTANCE_ID): {
                    'PSMAR20': ['BIGGER',0.02],
                    'VSMAR60': ['BIGGER', 10],
                    'TRADINGVALUE': ['BIGGER',1]
    },
}


COND_TEST_PRH1 = {
        '%s01'%(INSTANCE_ID): {
                                'PSMAR20': ['BIGGER',0.02],
                                'VSMAR60': ['BIGGER', 10],
                                'TRADINGVALUE': ['BIGGER',1]
                                                                            },


}

COND_TEST_PRH2 = {
        '%s01'%(INSTANCE_ID): {
                                'PSMAR20': ['BIGGER',0.02],
                                'VSMAR60': ['BIGGER', 11],
                                'TRADINGVALUE': ['BIGGER',1]
                                                                            },


}
COND_TEST_PRH3 = {
        '%s01'%(INSTANCE_ID): {
                                'PSMAR20': ['BIGGER',0.02],
                                'VSMAR60': ['BIGGER', 12],
                                'TRADINGVALUE': ['BIGGER',1]
                                                                            },


}
COND_TEST_PRH4 = {
        '%s01'%(INSTANCE_ID): {
                                'PSMAR20': ['BIGGER',0.02],
                                'VSMAR60': ['BIGGER', 13],
                                'TRADINGVALUE': ['BIGGER',1]
                                                                            },


}

COND_TEST_PRH5 = {
        '%s01'%(INSTANCE_ID): {
                                'PSMAR20': ['BIGGER',0.02],
                                'VSMAR60': ['BIGGER', 14],
                                'TRADINGVALUE': ['BIGGER',1]
                                                                            },


}


COND_TEST_PRH6 = {
    '%sB01'%(INSTANCE_ID): {
                    'PSMAR60': ['BIGGER',0.02],
                    'VSMAR20': ['BIGGER', 10],
                    'VSMAR5': ['BIGGER', 1],
                    'TRADINGVALUE': ['BIGGER',1]
    },
}

COND_TEST_PRH7 = {
    '%sB01'%(INSTANCE_ID): {
                    'PSMAR60': ['BIGGER',0.02],
                    'VSMAR20': ['BIGGER', 10],
                    'VSMAR5':['BIGGER', 1.5],
                    'TRADINGVALUE': ['BIGGER',1]
    },
}



COND_TEST_PRH9 = {
        '%s01'%(INSTANCE_ID): {
                                'PSMAR20': ['BIGGER',0.02],
                                'VSMAR60': ['BIGGER', 10],
                                'CLOSE': ['SMALLER_P', 0.08],
                                'TRADINGVALUE': ['BIGGER',1]
                                                                            },


}

