import pandas as pd
import jazzstock_bot
import os

pd.options.display.max_rows = 500
pd.options.display.max_columns= 500
pd.options.display.expand_frame_repr=False

def main(TIME_START, COND_LABEL):

    path_account = os.path.join(jazzstock_bot.PATH_SIMULATION,'result',TIME_START,COND_LABEL)


    ACC_HOLD_PURCHASED = 0
    ACC_PROFIT_EXPECTED = 0
    ACC_PROFIT_REALIZED = 0
    ACC_HIST_PURCHASED = 0
    ACC_HIST_SELLED = 0
    ACC_TOTAL_PROFIT = 0
    ACC_TOTAL_PURCHASED = 0

    for eachcsv in os.listdir(path_account):
        if('.csv' in eachcsv):
            COLUMNS = ['STOCKCODE','DATE','HOLDPURCHASED','HOLDAMOUNT','PROFIT','HISTPURCHASED','HISTSELLED','CLOSEDAY']
            COLUMNS_NUMERIC = COLUMNS[2:]
            df = pd.read_csv(os.path.join(path_account,eachcsv), header=None, dtype=str)
            df.columns = COLUMNS
            for each in COLUMNS_NUMERIC:
                df[each] = df[each].astype('float')


            df['AVG']=df.HOLDPURCHASED / df.HOLDAMOUNT
            df['PROFIT_EXPECTED'] =  (df.CLOSEDAY * df.HOLDAMOUNT - df.HOLDPURCHASED)

            HOLD_PURCHASED= 0 or df.HOLDPURCHASED.tail(1).values[0]
            PROFIT_EXPECTED= 0 or (df.CLOSEDAY * df.HOLDAMOUNT - df.HOLDPURCHASED).tail(1).values[0]

            PROFIT_REALIZED= 0 or df.PROFIT.sum()
            HIST_PURCHASED= 0 or df.HISTPURCHASED.tail(1).values[0]
            HIST_SELLED= 0 or df.HISTSELLED.tail(1).values[0]       # 요건 수수료 산출할때 필요


            TOTAL_PURCHASED = HIST_PURCHASED+HOLD_PURCHASED
            TOTAL_PROFIT = PROFIT_EXPECTED + PROFIT_REALIZED

            # 개별종목 정보
            # RECOVERY_RATE = HIST_PURCHASED/TOTAL_PURCHASED if TOTAL_PURCHASED != 0 else 0
            # PROFIT_EXPECTED_RATIO = PROFIT_EXPECTED/HOLD_PURCHASED if HOLD_PURCHASED != 0 else 0
            # PROFIT_REALIZED_RATIO = PROFIT_REALIZED/HIST_PURCHASED if HIST_PURCHASED != 0 else 0
            # PROFIT_TOTAL_RATIO = TOTAL_PROFIT/TOTAL_PURCHASED if TOTAL_PURCHASED != 0 else 0
            # print(df.tail(10))
            # print('-'*60)
            # print('회수율_자금: {:+.4f} ( {:>10,.0f} / {:>10,.0f} )'.format(RECOVERY_RATE, HIST_PURCHASED, TOTAL_PURCHASED))
            # print('수익률_기대: {:+.4f} ( {:>10,.0f} / {:>10,.0f} )'.format(PROFIT_EXPECTED_RATIO, PROFIT_EXPECTED, HOLD_PURCHASED))
            # print('수익률_실현: {:+.4f} ( {:>10,.0f} / {:>10,.0f} )'.format(PROFIT_REALIZED_RATIO, PROFIT_REALIZED, HIST_PURCHASED))
            # print('수익률_도합: {:+.4f} ( {:>10,.0f} / {:>10,.0f} )'.format(PROFIT_TOTAL_RATIO, TOTAL_PROFIT, TOTAL_PURCHASED))
            # print('-'*60,'\n')

            ACC_HOLD_PURCHASED += HOLD_PURCHASED
            ACC_PROFIT_EXPECTED += PROFIT_EXPECTED
            ACC_PROFIT_REALIZED += PROFIT_REALIZED
            ACC_HIST_PURCHASED += HIST_PURCHASED
            ACC_HIST_SELLED += HIST_SELLED
            ACC_TOTAL_PROFIT += TOTAL_PROFIT
            ACC_TOTAL_PURCHASED += TOTAL_PURCHASED

    ACC_RECOVERY_RATE = ACC_HIST_PURCHASED / ACC_TOTAL_PURCHASED
    ACC_PROFIT_EXPECTED_RATIO = ACC_PROFIT_EXPECTED / ACC_HOLD_PURCHASED
    ACC_PROFIT_REALIZED_RATIO = ACC_PROFIT_REALIZED / ACC_HIST_PURCHASED
    ACC_PROFIT_TOTAL_RATIO = ACC_TOTAL_PROFIT / ACC_TOTAL_PURCHASED

    print('-'*60)
    print('회수율_자금: {:+.4f} ( {:>10,.0f} / {:>10,.0f} )'.format(ACC_RECOVERY_RATE, ACC_HIST_PURCHASED, ACC_TOTAL_PURCHASED))
    print('수익률_기대: {:+.4f} ( {:>10,.0f} / {:>10,.0f} )'.format(ACC_PROFIT_EXPECTED_RATIO, ACC_PROFIT_EXPECTED, ACC_HOLD_PURCHASED))
    print('수익률_실현: {:+.4f} ( {:>10,.0f} / {:>10,.0f} )'.format(ACC_PROFIT_REALIZED_RATIO, ACC_PROFIT_REALIZED, ACC_HIST_PURCHASED))
    print('수익률_도합: {:+.4f} ( {:>10,.0f} / {:>10,.0f} )'.format(ACC_PROFIT_TOTAL_RATIO, ACC_TOTAL_PROFIT, ACC_TOTAL_PURCHASED))
    print('-'*60,'\n')

# main(TIME_START='DEBUG', COND_LABEL='TP')
# main(TIME_START = '20200824000959_159', COND_LABEL = 'TA')
# main(TIME_START = '20200824000959_159', COND_LABEL = 'TC')
# main(TIME_START = '20200824000959_159', COND_LABEL = 'TD')
# main(TIME_START = '20200824000959_159', COND_LABEL = 'TP')

main(TIME_START = '20200824115759_95', COND_LABEL = 'TA')
main(TIME_START = '20200824115759_95', COND_LABEL = 'TC')
main(TIME_START = '20200824115759_95', COND_LABEL = 'TD')
main(TIME_START = '20200824115759_95', COND_LABEL = 'TP')


main(TIME_START = '20200825010212_34', COND_LABEL = 'TA')
main(TIME_START = '20200825010212_34', COND_LABEL = 'TC')
main(TIME_START = '20200825010212_34', COND_LABEL = 'TD')
main(TIME_START = '20200825010212_34', COND_LABEL = 'TP')




#
# main(TIME_START = 'FOR_80_157', COND_LABEL = 'TA')
# main(TIME_START = 'INS_80_156', COND_LABEL = 'TA')
# main(TIME_START = 'PER_80_156', COND_LABEL = 'TA')
#
# main(TIME_START = 'FOR_80_157', COND_LABEL = 'TB')
# main(TIME_START = 'INS_80_156', COND_LABEL = 'TB')
# main(TIME_START = 'PER_80_156', COND_LABEL = 'TB')
#
# main(TIME_START = 'FOR_80_157', COND_LABEL = 'TC')
# main(TIME_START = 'INS_80_156', COND_LABEL = 'TC')
# main(TIME_START = 'PER_80_156', COND_LABEL = 'TC')
#
# main(TIME_START = 'FOR_80_157', COND_LABEL = 'TD')
# main(TIME_START = 'INS_80_156', COND_LABEL = 'TD')
# main(TIME_START = 'PER_80_156', COND_LABEL = 'TD')
#
# main(TIME_START = 'FOR_80_157', COND_LABEL = 'TE')
# main(TIME_START = 'INS_80_156', COND_LABEL = 'TE')
# main(TIME_START = 'PER_80_156', COND_LABEL = 'TE')
#
#
#
# main(TIME_START = 'FOR_80_95', COND_LABEL = 'TA')
# main(TIME_START = 'INS_80_94', COND_LABEL = 'TA')
# main(TIME_START = 'PER_80_94', COND_LABEL = 'TA')
#
# main(TIME_START = 'FOR_80_95', COND_LABEL = 'TB')
# main(TIME_START = 'INS_80_94', COND_LABEL = 'TB')
# main(TIME_START = 'PER_80_94', COND_LABEL = 'TB')
#
# main(TIME_START = 'FOR_80_95', COND_LABEL = 'TC')
# main(TIME_START = 'INS_80_94', COND_LABEL = 'TC')
# main(TIME_START = 'PER_80_94', COND_LABEL = 'TC')
#
# main(TIME_START = 'FOR_80_95', COND_LABEL = 'TD')
# main(TIME_START = 'INS_80_94', COND_LABEL = 'TD')
# main(TIME_START = 'PER_80_94', COND_LABEL = 'TD')
#
# main(TIME_START = 'FOR_80_95', COND_LABEL = 'TE')
# main(TIME_START = 'INS_80_94', COND_LABEL = 'TE')
# main(TIME_START = 'PER_80_94', COND_LABEL = 'TE')
#
#
# main(TIME_START = 'FOR_80_34', COND_LABEL = 'TA')
# main(TIME_START = 'INS_80_33', COND_LABEL = 'TA')
# main(TIME_START = 'PER_80_33', COND_LABEL = 'TA')
#
# main(TIME_START = 'FOR_80_34', COND_LABEL = 'TB')
# main(TIME_START = 'INS_80_33', COND_LABEL = 'TB')
# main(TIME_START = 'PER_80_33', COND_LABEL = 'TB')
#
# main(TIME_START = 'FOR_80_34', COND_LABEL = 'TC')
# main(TIME_START = 'INS_80_33', COND_LABEL = 'TC')
# main(TIME_START = 'PER_80_33', COND_LABEL = 'TC')
#
# main(TIME_START = 'FOR_80_34', COND_LABEL = 'TD')
# main(TIME_START = 'INS_80_33', COND_LABEL = 'TD')
# main(TIME_START = 'PER_80_33', COND_LABEL = 'TD')
#
# main(TIME_START = 'FOR_80_34', COND_LABEL = 'TE')
# main(TIME_START = 'INS_80_33', COND_LABEL = 'TE')
# main(TIME_START = 'PER_80_33', COND_LABEL = 'TE')




# print("ndf.HOLDPURCHASED.sum())
# print((ndf.CLOSEDAY*ndf.HOLDAMOUNT).sum())
# print(ndf.HISTPURCHASED.sum())
# print(ndf.HISTSELLED.sum())
# print(df.PROFIT.sum())
#
#
# 2371258.0
# 2091215.0
# 2074560.0
# 333479.6798245616
#
# 109312224.50980392
# 102113064.0
# 76109580.0
# 20612447.596037827
#
#
# HISTPURCHASED에 현재 보유금액은 별도로, 매도가 발생했을때만 넣는걸로 수정해야함.
# FINISHED PURCHASED 를 새로 만들어야함... 일정산으로 바뀌니까 이게 사라졌음


