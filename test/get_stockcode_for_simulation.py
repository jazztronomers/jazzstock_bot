import common.connector_db as db
import sys

'''
BASH SCRIPT 로 LIST 를 넘겨야 할때 사용할 스크립트
'''

COUNT = sys.argv[1]
GROUP = sys.argv[2]

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

sl = db.selectSingleColumn(query)
rt = ' '.join(sl)
print(rt)
