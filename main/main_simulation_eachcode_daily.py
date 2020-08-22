from datetime import datetime
import argparse
st1 = datetime.now()
import util.util as ut
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
parser.add_argument('--account_path', type=str, default='account.csv', metavar='a',
                    help='account_path')






args = parser.parse_args()

STOCKCODE = args.stockcode
DATE_IDX  = args.date_idx
DATE      = ut.index_to_date(DATE_IDX)
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


DATE = ut.index_to_date(DATE_IDX)
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
f = open(PATH_ACCOUNT,'a')
f.write(f'{STOCKCODE},{DATE},{hold_purchased},{amount},{profit},{purchased},{selled},{close_day}\n')
f.close()

print(datetime.now()-st1)
print(datetime.now()-st2)
print(datetime.now()-st3)
print(datetime.now()-st4)
print(datetime.now()-st5)
print(datetime.now()-st6)
