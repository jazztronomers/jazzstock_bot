from datetime import datetime
st0 = datetime.now()
import argparse
st1 = datetime.now()
import common.connector_db as db
st2 = datetime.now()
import config.condition as cd
st3 = datetime.now()
from crawl.jazzstock_core_simulation import JazzstockCoreSimulationCustom
st4 = datetime.now()
'''

특정종목, 특정일자(하루)에 대해서 시뮬레이션 실행

'''

parser = argparse.ArgumentParser(description='Conditionally get Stockcode List')
parser.add_argument('--stockcode', type=str, default='079940', metavar='s',
                    help='stockcode')
parser.add_argument('--date_idx', type=int, default=0, metavar='d',
                    help='dateidx')
parser.add_argument('--purchased', type=int, default=0, metavar='p',
                    help='매수금액')
parser.add_argument('--amount', type=int, default=0, metavar='a',
                    help='매수수량')

parser.add_argument('--histpurchased', type=int, default=0, metavar='p',
                    help='누적매수금액')
parser.add_argument('--histselled', type=int, default=0, metavar='a',
                    help='누적매도금액')


parser.add_argument('--condition_label', type=str, default='TP', metavar='c',
                    help='conditon_label')
parser.add_argument('--account_path', type=str, default='account_<stockcode>.csv', metavar='a',
                    help='account_path')


def date_to_index(date):
    cnt = db.selectSingleValue("SELECT CNT FROM jazzdb.T_DATE_INDEXED WHERE 1=1 AND DATE = '%s'"%(date))
    return cnt

def index_to_date(idx):
    thedate = db.selectSingleValue("SELECT CAST(DATE AS CHAR) AS DATE FROM jazzdb.T_DATE_INDEXED WHERE 1=1 AND CNT = '%s'"%(idx))
    return thedate




args = parser.parse_args()

STOCKCODE = args.stockcode
DATE_IDX  = args.date_idx
DATE      = index_to_date(DATE_IDX)
PURCHASED = args.purchased
AMOUNT    = args.amount
HISTPURCHASED= args.histpurchased
HISTSELLED= args.histselled
COND= cd.condition_dict[args.condition_label]

PATH_ACCOUNT = args.account_path

st5 = datetime.now()


''' jazzstock_bot/simulation/<time>/<rule>/account.csv 
                                           <stockcode>/buysell.log
                                                       daily.log '''


st6 = datetime.now()

t = JazzstockCoreSimulationCustom(stockcode      = STOCKCODE,
                                  condition_buy  = COND,
                                  the_date       = DATE,
                                  the_date_index = DATE_IDX,
                                  purchased      = PURCHASED,
                                  amount         = AMOUNT,
                                  hist_purchased = HISTPURCHASED,
                                  hist_selled    = HISTSELLED,)


hold_purchased, amount, profit, purchased, selled, close_day, = t.simulate()

st7 = datetime.now()
f = open(PATH_ACCOUNT.replace('<stockcode>',STOCKCODE),'a')
f.write(f'{STOCKCODE},{DATE},{hold_purchased},{amount},{profit},{purchased},{selled},{close_day}\n')
f.close()

st8 = datetime.now()
print('='*60)
print(STOCKCODE, DATE_IDX)
print('='*60)
print('IMPORT ARGPARSE', st1-st0)
print('IMPORT UTIL    ', st2-st1)
print('IMPORT COND    ', st3-st2)
print('IMPORT OBJECT  ', st4-st3)
print('PARSE ARG      ', st5-st4)
print('IDX TO DATE    ', st6-st5)
print('SIMULATE       ', st7-st6)
print('APPEND ROW     ', st8-st7)
print('TOTAL          ', st8-st0)


# IMPORT ARGPARSE 0:00:00.027999
# IMPORT UTIL     0:00:00.853000
# IMPORT COND     0:00:00.001000
# IMPORT OBJECT   0:00:00.481000
# PARSE ARG       0:00:00.246052
# IDX TO DATE     0:00:00.013980
# SIMULATE        0:00:00.542543
# APPEND ROW      0:00:00.542543