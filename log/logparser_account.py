import os
import sys
import pandas as pd


PATH_ROOT= os.getcwd()
PATH_SUBDIR = 'simulation'
PATH_LABEL= sys.argv[1] if len(sys.argv) > 1 else 'A'
PATH_LOG = os.path.join(PATH_ROOT, PATH_SUBDIR, PATH_LABEL)


# ['* WHOLE_T01A01',           '009290', '2020-08-03', '11162', '9110', '-2052', '46812', '820828.0', '867640.0', '5.703', '208880', '-7187']
# ['* DAILY_T01_거래량동반돌파, 104480,  '2020-08-05', 1315530', '1206000', '-109530', '242815', '1315530', '-145645']

COLUMNS = ['STOCKCODE', 'DATE', 'CLOSE', 'AVG', 'PROFIT_REALTIME', 'PROFIT_REALIZED', 'CUM_PURCHASED', 'CUM_SELLED', 'PROFIT_RATIO', 'PURCHASED_MAX', 'LOSS_MIN']
# COLUMNS = ['STOCKCODE', 'DATE', 'CLOSE', 'AVG', 'PROFIT_REALTIME', 'PROFIT_REALIZED', 'CUM_PURCHASED', 'CUM_SELLED']
COLUMNS_NUMERIC = COLUMNS[2:]

df = pd.DataFrame(columns=COLUMNS)

for each in os.listdir(PATH_LOG):
    f = open(os.path.join(PATH_LOG, each), 'r')
    for eachline in f.readlines():
        temp = eachline.replace('\n','')
        if '* DAILY' in temp:
            

            df.loc[len(df)]=temp.split('\t')[1:]
    f.close()


print(df.sort_values('DATE').reset_index(drop=True).tail(50))




