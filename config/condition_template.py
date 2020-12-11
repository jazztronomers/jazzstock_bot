'''

KEY값으로 쓸 수 있는것들...

'''

# ['DATE', 'TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME', 'PSMA5', 'PSMA20', 'PSMA60', 'PSMAR5', 'PSMAR20',
#  'PSMAR60', 'VSMA5', 'VSMA20', 'VSMA60', 'VSMAR5', 'VSMAR20', 'VSMAR60', 'BBU', 'BBL', 'BBS', 'BBW', 'BBP', 'K',
#  'D', 'J', 'OBV', 'CLOSEDIFF', 'RSI', 'TRADINGVALUE']

# ['01D_DATE', '01D_OPEN', '01D_HIGH', '01D_LOW', '01D_CLOSE', '01D_VOLUME',
#  '01D_BBP', '01D_BBW', '01D_BBU', '01D_BBL',
#  '01D_K', '01D_D', '01D_J',
#  '01D_I1', '01D_I5', '01D_I20', '01D_I60', '01D_F1', '01D_F5', '01D_F20', '01D_F60',
#  '01D_S1', '01D_S5', '01D_S20', '01D_S60', '01D_YG1', '01D_YG5', '01D_YG20', '01D_YG60',
#  '01D_T1', '01D_T5', '01D_T20', '01D_T60', '01D_FN1', '01D_FN5', '01D_FN20', '01D_FN60',
#  '01D_RSI', '05D_HIGH', '05D_LOW', '60D_HIGH', '60D_LOW']


# condition_dict 작성요령
# 절대적으로 숫자가 적을것 같은 조건을 상위에 배치해서 불필요한 연산을 줄인다

condition_template={

    'CLOSE': ['SMALLER_P', '05D_HIGH',0.10],        # 5분봉 종가가 5일간 최고점보다 10% 낮을때 !
    'CLOSE': ['BIGGER_P',  '05D_LOW', 0.10],        # 5분봉 종가가 5일간 최저점봗  10% 높을때 !
    'PSMAR60': ['BIGGER', 0.02],                    # 설명생략
    'VSMAR20': ['BIGGER', 5],                       # 설명생략
    'TRADINGVALUE': ['BIGGER', 1],                  # 거래대금 1억이상
    'CLOSE': ['BETWEEN', '05D_LOW', '05D_HIGH'],    # 5일저점 및 5일고점 사이일때
    'CLOSE': ['BETWEEN', '05D_HIGH','05D_LOW'],     # 5일저점 및 5일고점 사이일때, 위에꺼랑 똑같음, 순서 상관 X
    '01D_I1': ['BIGGER', 0],                        # 기관최근1거래일의 수급이 양인경우
    'VOLUME': ['BIGGER', '20D_85QTILE_VOL'],        # 5분봉 거래량이 최근 20거래일 거래량 상위 15% 보다 클때.
}





