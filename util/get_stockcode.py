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




def get_stockcode(whom=WHOM, window=WINDOW, row_num_from=ROW_NUM_FROM, row_num_to=ROW_NUM_TO, date_idx =DATE_IDX,
                  min_market_cap=MIN_MARKET_CAP, descending=DESCENDING):
    '''
    :param whom 어느주체를 선택 할지 ( ins, for, yg, per, samo )
    :param window 수급순위 뽑을때 windows size, default 5
    :param row_num_from
    :param row_num_to
    :param date_idx
    :param min_market_cap
    :param descending
    '''

    WINDOW_DICT = {

        'ins': 'I',
        'for': 'F',
        'yg': 'YG',
        'per': 'PS',
        'samo': 'S'

    }
    query = f'''

    SELECT STOCKCODE
    FROM
    (
        SELECT STOCKCODE,
            ROW_NUMBER() OVER (PARTITION BY DATE ORDER BY {WINDOW_DICT[whom]}{window} {descending}) AS RN
        FROM jazzdb.T_STOCK_SND_ANALYSIS_RESULT_TEMP
        JOIN jazzdb.T_DATE_INDEXED USING (DATE)
        JOIN jazzdb.T_STOCK_MC USING (STOCKCODE, DATE)
        WHERE 1=1
        AND CNT = {date_idx}
        AND MC > {min_market_cap}          # 1300종목
    ) A
    WHERE 1=1 
    AND RN BETWEEN {row_num_from} AND {row_num_to}

    '''



    if args.verbose:
        print(f'QUERY:\n{query}\n===========================================')

    stockcode_list = db.selectSingleColumn(query)  # SELECT 결과를 리스트로 받음
    return stockcode_list



if __name__ =='__main__':

    # COMMAND LINE 에서 실행시, RETURN 값을 출력해서
    # STDOUT parsing해서 값을 가져가기 위함
    stockcode_list=get_stockcode()
    rt = SEPERATOR.join(stockcode_list)
    print(rt)



