import pandas as pd
import os
import argparse
SEPERATOR = ' '


parser = argparse.ArgumentParser(description='Conditionally get Stockcode List')
parser.add_argument('--stockcode', type=str, default='289010', metavar='w',
                    help='stockcode')

parser.add_argument('--account_path', type=str, default='account.csv', metavar='n',
                    help='/workspace/jazzstock_bot/simulation/result/TA/account.csv')


args = parser.parse_args()




def get_latest_info_from_account(stockcode, path_account):
    '''
    account.csv 를 읽어서 가장 최근기준 amount가 0 이상인 종목을 리스트로 반환함
    '''

    COLUMNS = ['STOCKCODE', 'DATE', 'HOLDPURCHASED', 'HOLDAMOUNT', 'PROFIT', 'HISTPURCHASED', 'HISTSELLED', 'CLOSEDAY']
    COLUMNS_NUMERIC = COLUMNS[2:]

    if os.path.isfile(path_account):
        df = pd.read_csv(path_account, header=None, dtype=str)
        df.columns = COLUMNS
        for each in COLUMNS_NUMERIC:
            df[each] = df[each].astype('float')


        # 최근일자 조회
        df = df[df['DATE'] == df['DATE'].max()]
        df = df[df['STOCKCODE']==stockcode][['HOLDPURCHASED', 'HOLDAMOUNT', 'PROFIT', 'HISTPURCHASED', 'HISTSELLED']]

        if len(df)>0:
            return list(df.tail(1).values[0])
        else:
            return []
    else:
        return []


if __name__ == '__main__':
    # COMMAND LINE 에서 실행시, RETURN 값을 출력해서
    # STDOUT parsing해서 값을 가져가기 위함
    stockcode_list = get_latest_info_from_account(args.stockcode, args.account_path)
    rt = SEPERATOR.join([str(int(x)) for x in stockcode_list])
    print(rt)

