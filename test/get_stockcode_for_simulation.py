import common.connector_db as db
import argparse

'''
COMMAND LINE에서 ARGV를 받아서 쿼리를 실행하여 반환 받은 결과를
BASH SCRIPT 로 SPACE SPLITED STRING (LIST) ARGV 넘겨야 할때 사용함
'''

parser = argparse.ArgumentParser(description='Conditionally get Stockcode List')
parser.add_argument('--whom', type=str, default='ins', metavar='w',
                    help='window, option:ins, for, yg, samo')

parser.add_argument('--window', type=int, default=5, metavar='n',
                    help='window, option:ins, for, yg, samo')

parser.add_argument('--seperator', type=str, default='s', metavar='s',
                     help='s: space separated list, c: comma separated list,')

parser.add_argument('--row_num_from', type=int, default=0, metavar='f',
                     help='row_num_from')
parser.add_argument('--row_num_to', type=int, default=20, metavar='t',
                     help='row_num_to')

parser.add_argument('--date_idx', type=int, default=0, metavar='d',
                     help='date_idx')
parser.add_argument('--min_market_cap', type=int, default=1, metavar='m',
                     help='min_market_cap')


parser.add_argument('--descending', type=int, default=1, metavar='m',
                     help='descending, 0 or 1')
parser.add_argument('--verbose', type=int, default=0, metavar='v',
                     help="print query or not, 0 or 1")

args = parser.parse_args()



WHOM = args.whom
WINDOW = args.window
SEPERATOR = ',' if args.seperator=='c' else ' '
ROW_NUM_FROM= args.row_num_from
ROW_NUM_TO= args.row_num_to
DATE_IDX = args.date_idx
MIN_MARKET_CAP = args.min_market_cap
DESCENDING = 'DESC' if args.descending else 'ASC'


WINDOW_DICT = {

    'ins':'I',
    'for':'F',
    'yg':'YG',
    'per':'PS',
    'samo':'S'

}
query = f'''

SELECT STOCKCODE
FROM
(
    SELECT STOCKCODE,
        ROW_NUMBER() OVER (PARTITION BY DATE ORDER BY {WINDOW_DICT[WHOM]}{WINDOW} {DESCENDING}) AS RN
    FROM jazzdb.T_STOCK_SND_ANALYSIS_RESULT_TEMP
    JOIN jazzdb.T_DATE_INDEXED USING (DATE)
    JOIN jazzdb.T_STOCK_MC USING (STOCKCODE, DATE)
    WHERE 1=1
    AND CNT = {DATE_IDX}
    AND MC > {MIN_MARKET_CAP}          # 1300종목
) A
WHERE 1=1 
AND RN BETWEEN {ROW_NUM_FROM} AND {ROW_NUM_TO}

'''
if args.verbose:

    print(f'QUERY:\n{query}\n===========================================')

sl = db.selectSingleColumn(query)         # SELECT 결과를 리스트로 받음
rt = SEPERATOR.join(sl)
print(rt)


