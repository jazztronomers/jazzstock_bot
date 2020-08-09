import os
import sys
import pandas as pd


PATH_ROOT= '/workspace/jazzstock_bot/simulation'
PATH_LABEL= sys.argv[1] if len(sys.argv) > 1 else 'TA'
PATH_SUBDIR = 'result_%s'%(sys.argv[2]) if len(sys.argv) > 2 else 'result_template'

PATH_LOG = os.path.join(PATH_ROOT, PATH_SUBDIR, PATH_LABEL)


# ['* WHOLE_T01A01',           '009290', '2020-08-03', '11162', '9110', '-2052', '46812', '820828.0', '867640.0', '5.703', '208880', '-7187']
# ['* DAILY_T01_거래량동반돌파, 104480,  '2020-08-05', 1315530', '1206000', '-109530', '242815', '1315530', '-145645']

COLUMNS = ['STOCKCODE', 'DATE', 'CLOSE', 'AVG', 'PROFIT_REALTIME', 'PROFIT_REALIZED', 'CUM_PURCHASED', 'CUM_SELLED', 'PROFIT_RATIO', 'PURCHASED_MAX', 'LOSS_MIN']
COLUMNS_NUMERIC = COLUMNS[2:]
df = pd.DataFrame(columns=COLUMNS)


for each in os.listdir(PATH_LOG):
    f = open(os.path.join(PATH_LOG, each), 'r')
    for eachline in f.readlines():
        temp = eachline.replace('\n','')
        if '* DAILY' in temp:
            

            df.loc[len(df)]=temp.split('\t')[1:]
    f.close()


for each in COLUMNS_NUMERIC:
        df[each] = df[each].astype('float')


result_df = df.groupby(['DATE']).sum()[['CLOSE', 'AVG', 'PROFIT_REALTIME', 'CUM_PURCHASED', 'PROFIT_REALIZED' ]]
result_df['PROFIT_HIST']=result_df['PROFIT_REALTIME']+result_df['PROFIT_REALIZED']

# MDD = result_df['PROFIT_HIST'].min()



result_dic = result_df.iloc[-1].to_dict()
recovery_rate=result_dic['CUM_PURCHASED'] / (result_dic['CLOSE']+result_dic['CUM_PURCHASED'])
profit_ratio_net= result_dic['PROFIT_HIST'] / (result_dic['CLOSE']+result_dic['CUM_PURCHASED'])
profit_ratio_realized= result_dic['PROFIT_REALIZED'] / result_dic['CUM_PURCHASED']
profit_ratio_expected= result_dic['PROFIT_REALTIME'] / result_dic['CLOSE']

print(PATH_LABEL)
print('-'*60)
print('회수율_자금: {:+.4f} ( {:>10,.0f} / {:>10,.0f} )'.format(recovery_rate, result_dic['CUM_PURCHASED'], result_dic['CLOSE']+result_dic['CUM_PURCHASED']))
print('수익률_기대: {:+.4f} ( {:>10,.0f} / {:>10,.0f} )'.format(profit_ratio_expected, result_dic['PROFIT_REALTIME'], result_dic['CLOSE']))
print('수익률_실현: {:+.4f} ( {:>10,.0f} / {:>10,.0f} )'.format(profit_ratio_realized, result_dic['PROFIT_REALIZED'], result_dic['CUM_PURCHASED']))
print('수익률_도합: {:+.4f} ( {:>10,.0f} / {:>10,.0f} )'.format(profit_ratio_net, result_dic['PROFIT_HIST'], result_dic['CLOSE']+result_dic['CUM_PURCHASED']))
print('-'*60,'\n')
