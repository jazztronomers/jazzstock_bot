import common.connector_db as db
import argparse
import util.util as ut
import os
import sys
import config.condition as cd
from crawl.jazzstock_core_simulation import JazzstockCoreSimulationCustom
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
parser.add_argument('--condition_label', type=str, default='TP', metavar='c',
                    help='conditon_label')
parser.add_argument('--account_path', type=str, default=os.getcwd(), metavar='a',
                    help='account_path')






args = parser.parse_args()

STOCKCODE = args.stockcode
DATE_IDX  = args.date_idx
DATE      = ut.index_to_date(DATE_IDX)
PURCHASED = args.purchased
AMOUNT    = args.amount
COND= cd.condition_dict[args.condition_label]

PATH_OUTPUT = '' # account.csv, buysell.log, daily.log

''' jazzstock_bot/simulation/<time>/<rule>/account.csv 
                                           <stockcode>/buysell.log
                                                       daily.log '''


print(args)
print(sys.path)


for i in range(100, 0, -1):
    dt = ut.index_to_date(i)
    t = JazzstockCoreSimulationCustom(stockcode      = STOCKCODE,
                                      condition_buy  = COND,
                                      the_date       = dt,
                                      the_date_index = i,
                                      purchased      = PURCHASED,
                                      amount         = AMOUNT)


    hold_purchased, amount, profit, purchased, selled, close_day, = t.simulate()
    print(i, hold_purchased, amount, profit, purchased, selled, close_day)

# temp = list(stock_dic[stockcode])
# temp[0] = int(hold_purchased)
# temp[1] = int(amount)
# temp[2] = temp[2] + int(profit)
# temp[3] = temp[3] + purchased
# temp[4] = temp[4] + selled


#     stock_dic[stockcode] = tuple(temp)
#
#     PURCHASED_HOLD, AMOUNT_HOLD, PROFIT, _, _ = stock_dic[stockcode]
#     AVERAGE_HOLD, PURCHASED_CUM, SELL_CUM = summary(stock_dic[stockcode])
#
#     if AVERAGE_HOLD != 0:
#         PROFIT_RATIO = round((close_day - AVERAGE_HOLD) / close_day, 3) * 100
#     else:
#         PROFIT_RATIO = 0
#
#     PURCHASED_HIGH = max(PURCHASED_HIGH, PURCHASED_HOLD)
#     LOSS_HIGH = min(AMOUNT_HOLD * close_day - PURCHASED_HOLD, LOSS_HIGH)
#
#     record([stockcode, 0, 0], path_output)
#     print('* DAILY_%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%.3f\t%s\t%s' % (list(condition_buy.keys())[0],
#                                                                         stockcode,
#                                                                         the_date,
#                                                                         PURCHASED_HOLD,  # 보유금액
#                                                                         AMOUNT_HOLD * close_day,  # 평가금액
#                                                                         AMOUNT_HOLD * close_day - PURCHASED_HOLD,
#                                                                         # 기대수익
#                                                                         PROFIT,
#                                                                         PURCHASED_CUM,
#                                                                         SELL_CUM,
#                                                                         0 if PURCHASED_CUM == 0 else PROFIT / PURCHASED_CUM * 100,
#                                                                         PURCHASED_HIGH,
#                                                                         LOSS_HIGH))
#
#
#
#
#
# except Exception as e:
#     print('* ERROR %s, %s ' % (e, stockcode))