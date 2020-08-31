import os
import time
import psutil
import subprocess
import pandas as pd
import jazzstock_bot as jazzstock_bot
from datetime import datetime
from util.jazzstock_util_stockcode import *


def run_script(script_name='test_argv_printer.py', argument = ['--stockcode', '079940'], path_log_cond='./'):
    '''

    subprocess로 파이썬 스크립트를 실행해주는 함수

    :param script_name: 실행스크립트 파일 + 상대경로
    :param argument:    실행스크립트에 넘겨줄 argvment
    :param path_log_cond: 스크립트 실행 로그를 저장하는 경로
    :return:
    '''
    src_abs_path = os.path.join(PATH_ROOT, script_name)
    proc = subprocess.Popen(['python', '-u', src_abs_path] + argument, stdout=path_log_cond, stderr=path_log_cond, shell=True)
    return proc


def _should_run(stockcode_list_len, date_change=False):
    '''

    추가로 subprocess를 띄울지 판단하는 함수
    main 함수 내부함수로 신경 쓸 필요 없음

    :param stockcode_list_len:
    :param date_change: 일자변경여부 체크,
    :return:
    '''

    global process_q
    process_q = [p for p in process_q if psutil.pid_exists(p)]

    if date_change == True and len(process_q) > 0:
        return False

    elif len(process_q)<min(len_q,stockcode_list_len):
        time.sleep(0.1)
        return True

    else:
        if stockcode_list_len>1:
            time.sleep(1)

        return False


def get_stockcode_from_account(path_log_cond):
    '''
    account.csv 를 읽어서 가장 최근기준 amount가 0 이상인 종목을 리스트로 반환함
    '''

    stockcode_list = []
    for eachfile in os.listdir(path_log_cond):
        if '.csv' in eachfile:
            df = pd.read_csv(os.path.join(path_log_cond, eachfile), header=None, dtype=str)
            df.columns = COLUMNS
            for each in COLUMNS_NUMERIC:
                df[each] = df[each].astype('float')

            # 최근일자 조회
            df= df[df['DATE']==df['DATE'].max()]

            # amount가 0이 아닌애들만
            if df.HOLDAMOUNT.values[0]>0:
                stockcode_list.append(df.STOCKCODE.values[0])


    return stockcode_list


def main(date_idx_from, date_idx_to):
    for COND in ['TP','TA','TC','TD']:

        START = datetime.now()

        PATH_LOG_COND = os.path.join(os.path.join(PATH_LOG, COND))
        os.makedirs(PATH_LOG_COND, exist_ok=True)
        FILE_LOG_COND = open(os.path.join(PATH_LOG_COND, 'fulllog.log'),'a')
        PATH_ACCOUNT = os.path.join(os.path.join(PATH_LOG_COND, 'account_<stockcode>.csv'))


        for date_idx in range(date_idx_from, date_idx_to,-1):
            print(COND,date_idx, datetime.now()-START)

            while not _should_run(9999, date_change=True):
                pass

            params =dict(whom='for',
                         window=5,
                         descending='DESC',
                         row_num_from=0,
                         row_num_to=160,
                         date_idx =date_idx,
                         min_market_cap=1,
                         )

            # ==================================================================
            # EDU: 시뮬레이션 진행할 종목코드를 list 로 선언
            # ==================================================================
            stockcode_new = ['079940','093320']


            stockcode_acc = get_stockcode_from_account(PATH_LOG_COND)
            stockcode_list = list(stockcode_new)
            stockcode_list.extend(x for x in stockcode_acc if x not in stockcode_list)



            print('금일모니터링 종목 TOTAL', len(stockcode_list))

            for stockcode in stockcode_list:
                while not _should_run(stockcode_list_len=len(stockcode_list)):
                    pass

                # GEN OR READ EXISTS ACCOUNT FILE

                if os.path.isfile(PATH_ACCOUNT.replace('<stockcode>',stockcode)):
                    # print('HERE', stockcode)
                    df = pd.read_csv(PATH_ACCOUNT.replace('<stockcode>',stockcode),header=None, dtype=str)
                    df.columns=COLUMNS
                    for each in COLUMNS_NUMERIC:
                        df[each] = df[each].astype('float')
                else:
                    df = pd.DataFrame(columns=COLUMNS)

                if len(df[df['STOCKCODE']==stockcode])>0:
                    HOLD_PURCHASED = int(df[df['STOCKCODE']==stockcode].tail(1).HOLDPURCHASED)
                    HOLD_AMOUNT = int(df[df['STOCKCODE']==stockcode].tail(1).HOLDAMOUNT)
                    HISTPURCHASED = int(df[df['STOCKCODE'] == stockcode].tail(1).HISTPURCHASED)
                    HISTSELLED = int(df[df['STOCKCODE'] == stockcode].tail(1).HISTSELLED)

                else:
                    HOLD_PURCHASED = 0
                    HOLD_AMOUNT = 0
                    PROFIT = 0
                    HISTPURCHASED = 0
                    HISTSELLED = 0

                p = run_script('main_simulation_eachcode_daily.py', argument=['--stockcode', str(stockcode),\
                                                                              '--date_idx', str(date_idx),\
                                                                              '--purchased', str(HOLD_PURCHASED),\
                                                                              '--amount', str(HOLD_AMOUNT), \
                                                                              '--histpurchased', str(HISTPURCHASED), \
                                                                              '--histselled', str(HISTSELLED), \
                                                                              '--condition_label', str(COND),\
                                                                              '--account_path', PATH_ACCOUNT.replace('<stockcode>',stockcode)],
                               path_log_cond=FILE_LOG_COND)
                time.sleep(0.5)
                process_q.append(p.pid)





if __name__ == '__main__':

    for date_idx_from, date_idx_to in [(10,0)]:

        NOW = '%s_%s'%(datetime.now().strftime("%Y%m%d%H%M%S"), date_idx_from)
        print('start..... %s\n' % (NOW))
        PATH_ROOT = jazzstock_bot.PATH_MAIN
        PATH_LOG = os.path.join(jazzstock_bot.PATH_SIMULATION, 'result', NOW)
        COLUMNS = ['STOCKCODE', 'DATE', 'HOLDPURCHASED', 'HOLDAMOUNT', 'PROFIT', 'HISTPURCHASED', 'HISTSELLED', 'CLOSEDAY']
        COLUMNS_NUMERIC = COLUMNS[2:]
        os.makedirs(PATH_LOG, exist_ok=True)

        process_q, len_q = [], 10
        main(date_idx_from, date_idx_to)




