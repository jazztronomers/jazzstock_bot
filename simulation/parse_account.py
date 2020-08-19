import pandas as pd
import jazzstock_bot
import os

pd.options.display.max_rows = 500
pd.options.display.max_columns= 500
pd.options.display.expand_frame_repr=False

def main(TIME_START, COND_LABEL):

    path_account = os.path.join(jazzstock_bot.PATH_SIMULATION,'result',TIME_START,COND_LABEL,'account.csv')

    COLUMNS = ['STOCKCODE','DATE','HOLDPURCHASED','HOLDAMOUNT','PROFIT','HISTPURCHASED','HISTSELLED','CLOSEDAY']
    COLUMNS_NUMERIC = COLUMNS[2:]



    df = pd.read_csv(path_account, header=None, dtype=str)
    df.columns = COLUMNS
    for each in COLUMNS_NUMERIC:
        df[each] = df[each].astype('float')


    profit_sum = df.PROFIT.sum()

    df['PROFIT_REALIZED'] = (df.PROFIT.sum() / df['HISTPURCHASED']).round(3)
    df['AVG']= (df['HOLDPURCHASED'] / df['HOLDAMOUNT']).round(0)
    df['PROFIT_REALTIME']= (df['HOLDAMOUNT']*df['CLOSEDAY']-df['HOLDPURCHASED'])
    df['PROFIT_REALTIME_RATIO']= (df['PROFIT_REALTIME']/df['HOLDPURCHASED']).round(3)


    date_to, date_from = df.DATE.max(), df.DATE.min()


    result_df = df.groupby(['DATE']).sum()[['CLOSEDAY', 'AVG', 'PROFIT_REALTIME', 'HISTPURCHASED', 'PROFIT_REALIZED' ]]
    result_df['PROFIT_HIST']=result_df[result_df.index==date_to]['PROFIT_REALTIME'].sum() + df.PROFIT.sum()



    date_count = len(result_df.index)

    result_dic = result_df.iloc[-1].to_dict()
    recovery_rate=result_dic['HISTPURCHASED'] / (result_dic['CLOSEDAY']+result_dic['HISTPURCHASED'])
    profit_ratio_net= result_dic['PROFIT_HIST'] / (result_dic['CLOSEDAY']+result_dic['HISTPURCHASED'])
    profit_ratio_realized= profit_sum / result_dic['HISTPURCHASED']
    profit_ratio_expected= result_dic['PROFIT_REALTIME'] / result_dic['CLOSEDAY']



    print(COND_LABEL, '%s ~ %s (%s 거래일)'%(date_from, date_to, date_count))
    print('-'*60)
    print('회수율_자금: {:+.4f} ( {:>10,.0f} / {:>10,.0f} )'.format(recovery_rate, result_dic['HISTPURCHASED'], result_dic['CLOSEDAY']+result_dic['HISTPURCHASED']))
    print('수익률_기대: {:+.4f} ( {:>10,.0f} / {:>10,.0f} )'.format(profit_ratio_expected, result_dic['PROFIT_REALTIME'], result_dic['CLOSEDAY']))
    print('수익률_실현: {:+.4f} ( {:>10,.0f} / {:>10,.0f} )'.format(profit_ratio_realized, df.PROFIT.sum(), result_dic['HISTPURCHASED']))
    print('수익률_도합: {:+.4f} ( {:>10,.0f} / {:>10,.0f} )'.format(profit_ratio_net, result_dic['PROFIT_HIST'], result_dic['CLOSEDAY']+result_dic['HISTPURCHASED']))
    print('-'*60,'\n')

main(TIME_START = '20200819060343_94', COND_LABEL = 'TA')
main(TIME_START = '20200819060343_94', COND_LABEL = 'TB')
main(TIME_START = '20200819060343_94', COND_LABEL = 'TC')
main(TIME_START = '20200819060343_94', COND_LABEL = 'TD')
# main(TIME_START = '20200819000229_156', COND_LABEL = 'TE')

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


