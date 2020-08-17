import pandas as pd
import jazzstock_bot
import os

pd.options.display.max_rows = 500
pd.options.display.max_columns= 500
pd.options.display.expand_frame_repr=False

path_account = os.path.join(jazzstock_bot.PATH_SIMULATION,'result','20200818002246','TP','account.csv')

COLUMNS = ['STOCKCODE','DATE','HOLDPURCHASED','HOLDAMOUNT','PROFIT','HISTPURCHASED','HISTSELLED','CLOSEDAY']
COLUMNS_NUMERIC = COLUMNS[2:]



df = pd.read_csv(path_account, header=None, dtype=str)
df.columns = COLUMNS
for each in COLUMNS_NUMERIC:
    df[each] = df[each].astype('float')


df['PROFIT_REALIZED'] = (df['PROFIT'] / df['HISTPURCHASED']).round(3)
df['AVG']= (df['HOLDPURCHASED'] / df['HOLDAMOUNT']).round(0)
df['PROFIT_REALTIME']= (df['HOLDAMOUNT']*df['CLOSEDAY']-df['HOLDPURCHASED'])
df['PROFIT_REALTIME_RATIO']= (df['PROFIT_REALTIME']/df['HOLDPURCHASED']).round(3)



COLUMNS_PRINT_ORDERED = ['STOCKCODE','DATE','CLOSEDAY','AVG','PROFIT_REALTIME_RATIO','HOLDAMOUNT', 'HOLDPURCHASED',
                         'PROFIT_REALTIME','PROFIT_REALIZED','HISTPURCHASED','HISTSELLED','PROFIT']
print(df.sort_values(['DATE','STOCKCODE'],ascending=[True,True])[COLUMNS_PRINT_ORDERED])


ndf = df[df['DATE']=='2020-06-18']

print(ndf.HOLDPURCHASED.sum())
print((ndf.CLOSEDAY*ndf.HOLDAMOUNT).sum())
print(ndf.HISTSELLED.sum())
print(df.PROFIT.sum())



# HISTPURCHASED에 현재 보유금액은 별도로, 매도가 발생했을때만 넣는걸로 수정해야함.
# FINISHED PURCHASED 를 새로 만들어야함... 일정산으로 바뀌니까 이게 사라졌음


