import common.connector_db as db
import sys

'''
jazzstock_bot/common/connector_db.py 모듈을 읽어와서
db에 데이터를 python 자료형 (list, str, dataframe) 으로 반환 받는 간단예제

'''


GROUP = 'A'
COUNT = '50'

query = '''
SELECT STOCKCODE
FROM
(
    SELECT STOCKCODE, 
            CASE WHEN RN <= 120 THEN "A"
                 WHEN RN <= 240 THEN "B"
                 WHEN RN <= 360 THEN "C"
                 WHEN RN <= 480 THEN "D"
                 WHEN RN <= 600 THEN "E"
                 WHEN RN <= 720 THEN "F"
                 WHEN RN <= 840 THEN "G"
                 ELSE "H" END AS GRP
    FROM
    (
        SELECT STOCKCODE, 
            ROW_NUMBER() OVER (PARTITION BY DATE ORDER BY I5+F5 DESC) AS RN
        FROM jazzdb.T_STOCK_SND_ANALYSIS_RESULT_TEMP
        JOIN jazzdb.T_DATE_INDEXED USING (DATE)
        JOIN jazzdb.T_STOCK_MC USING (STOCKCODE, DATE)
        WHERE 1=1
        AND CNT = 0
        AND MC > 1          # 1300종목
    ) A
) B        
WHERE 1=1
AND GRP IN ('%s')
LIMIT %s
'''%(GROUP, COUNT)


# SELECT 결과를 리스트로 받음
# 딱 한컬럼만 받아오는 경우만 사용
result = db.selectSingleColumn(query)         
print(result)
print('-'*100)


# SELECT 결과를 PANDAS DATAFRAME으로 받음

STOCKCODE ='079940'
DATE = '2020-08-06'

query_df = '''
SELECT STOCKCODE, DATE, TIME, OPEN, HIGH, LOW, CLOSE, VOLUME 
FROM jazzdb.T_STOCK_OHLC_MIN
WHERE 1=1
AND STOCKCODE = '%s'
AND DATE = '%s'

'''%(STOCKCODE, DATE)

df = db.selectpd(query_df)



print(df.tail(10))

# DATAFRAME을 EXECL 파일로 저장
df.to_csv('./test/%s_%s.csv'%(STOCKCODE,DATE))


