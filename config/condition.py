import os
# Dataframe 에 거래대금 컬럼 추가, 거래량 지표를 사용할




# 5분봉 컬럼리스트: 
# Index(['DATE', 'TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME', 'PSMA5',
#        'PSMA20', 'PSMA60', 'PSMAR5', 'PSMAR20', 'PSMAR60', 'VSMA5', 'VSMA20',
#        'VSMA60', 'VSMAR5', 'VSMAR20', 'VSMAR60', 'BBU', 'BBL', 'BBS', 'BBW',
#        'BBP', 'K', 'D', 'J', 'OBV', 'CLOSEDIFF', 'RSI', 'TRADINGVALUE'],

if('INSTANCE_ID' in os.environ):
	
	INSTANCE_ID=os.environ['INSTANCE_ID']

else:
	INSTANCE_ID='T'


print(" * CONDITION INITIALIZED, instance_id: %s" %(INSTANCE_ID))


TESTCOND = {
    

    '%s_01_HIGH_VOL_PSMAR20'%(INSTANCE_ID): {
        
                    'VSMAR5':['BIGGER', 3],     
                    'PSMAR20':['BIGGER', 0.03],
                    'TRADINGVALUE':['BIGGER',1]  
    },
    
    '%s_02_BIG_K_VOL'%(INSTANCE_ID): {
                    'K': ['BIGGER' , 0.95],   
                    'VSMAR5':['BIGGER', 7],
                    'TRADINGVALUE':['BIGGER',2]  
    },
    
    '%s03_HIGH_VOL'%(INSTANCE_ID): {
        	    'PSMAR60':['BIGGER',0.02],
                    'VSMAR20':['BIGGER', 5],     
                    'TRADINGVALUE':['BIGGER',1]   
    },
    

    
    
#     'T04_DEBUG': {
#                     'CLOSE': ['BIGGER', 10000], 
#     },

}
