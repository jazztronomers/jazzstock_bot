import pandas as pd
import time
import warnings
import config.config as cf
import telepot
from datetime import datetime
from crawl.jazzstock_object import JazzstockObject


pd.options.display.max_rows = 500
pd.options.display.max_columns= 500
warnings.filterwarnings('ignore')
try:
	timedf = pd.read_csv('../config/time.csv', dtype=str)
except:
	timedf = pd.read_csv('config/time.csv', dtype=str)
tdic = {}
for tk, t1, t5, t15 in sorted(timedf.values.tolist()):
    tdic[str(tk).zfill(6)] = {'T1': str(t1).zfill(6), 'T5': str(t5).zfill(6), 'T15': str(t15).zfill(6)}

class JazzstockCoreRealtime:

    def __init__(self, stockcode_list, the_date, the_date_index):
        self.stock_dict = {}
        for stockcode in stockcode_list:
            self.stock_dict[stockcode] = JazzstockObject(stockcode, the_date=the_date, the_date_index=the_date_index)


    def initialize_dataframe(self):
        pass

    def run(self):
        '''

        :return:
        '''
        pass


    def debug(self):
        '''


        :return:
        '''
        pass


    def alert(self):
        '''

        실시간수집된 정보를 처리하여, 액션이 필요한 경우 MASTER로 MESSAGE를 보낸다
        여기서 MASTER는 실제 매수매도를 진행할 수 있는 윈도우서버
        또는 TELEGRAM BOT 서버를 얘기한다.

        :return:
        '''
        pass


class JazzstockCoreRealtimeNaver(JazzstockCoreRealtime):

    def __init__(self, stockcode_list=[], the_date = datetime.now().date(), the_date_index=0):
        super().__init__(stockcode_list, the_date, the_date_index)

        # OPTIONAL ==================================================================
        # NETWORK PARAMS, STANDALONE에서는 신경안써도됨
        self.MASTERIP = '127.0.0.1'
        # TELEGRAM ================================================
        self.TOKEN = cf.TELEBOT_TOKEN
        self.RECEIVER = cf.TELEBOT_ID
        self.BOT = telepot.Bot(self.TOKEN)
        # =========================================================



    def initialize_dataframe(self, cntto=0):
        '''
        초기화된 모든 종목에 대해서
        DB 특정거래일의 일봉정보와 분봉정보를 초기화하는 함수
        :return:
        '''

        listdf = pd.DataFrame()

        for eachcode in self.stock_dict.keys():
            self.stock_dict[eachcode].set_ohlc_min_from_db(cntto=cntto)
            self.stock_dict[eachcode].set_ohlc_day_from_db_include_index(cntto=cntto)
            self.stock_dict[eachcode].set_prev_day_index()
            listdf = listdf.append(self.stock_dict[eachcode].get_info())

        print('-'*100)
        print('전거래일 일봉기준 주가 및 지표 :')
        print(listdf.sort_values('BBP',ascending=True))
        print('-'*100)
        return listdf

    def debug(self):
        '''
        장종료후 디버깅목적함수
        최근거래일기준으로 개장후 2시간59분치 주가정보를 긁어옴
        '''
        
        print(' * RUN DEBUGGING')
        self.initialize_dataframe(cntto=1)
        
        for j in ['09','10','11']: # 9시부터 11시까지 1분단위로 디버깅
            for i in range(60):
                ntime = '%s%s00' % (str(j).zfill(2), str(i).zfill(2))
                for eachcode in self.stock_dict.keys():
                    try:
                        self.stock_dict[eachcode].set_ohlc_min_from_naver(is_debug=ntime, debug_date=self.stock_dict[eachcode].the_date)
                    except:
                        print("*** CONNECTION ERROR")
                        break
                    self.stock_dict[eachcode].set_candle_five(is_debug=ntime)
                    self.stock_dict[eachcode].fill_index()
                    msg = self.stock_dict[eachcode].check_status(logmode=1) # 현재는 출력만 하고 있지만, 본 함수에 alert 또는 매매로직을 구현하
                    if msg is not None:
                        self.send_message_telegram(msg)
                    time.sleep(0.1) # 대책없이 긁으면 네이버에 막힐 수 있으므로, 한종목당 0.1초 슬립
                
                print('\n\n  sleep 30 seconds ....\n\n')
                time.sleep(1) # 대책없이 긁으면 네이버에 막힐 수 있으므로, 한그룹 다돌면 30초씩 슬립하도록


    def run(self):
        '''
        WHILE LOOP 을 돌리면서, 1분마다 stock_dict을 looping하면서 분봉을 생성, 업데이트 하는 함수
        :return:
        '''
        marketready = datetime.strptime('08:40:00', '%H:%M:%S').time()
        marketopen = datetime.strptime('09:00:00', '%H:%M:%S').time()
        marketclose = datetime.strptime('15:30:00', '%H:%M:%S').time()
        
        self.initialize_dataframe(cntto=0)

        print(' * RUN CRAWLING')
        while True:

            now = datetime.now().time()
            if (marketopen <= now < marketclose):
                if str(now.second).zfill(2) == '05':
                    keytime = "%s%s00" % (str(now.hour).zfill(2), str(now.minute).zfill(2))

                    if (keytime not in tdic.keys()):
                        time.sleep(1)

                    else:

                        st = datetime.now()
                        for eachcode in self.stock_dict.keys():
                            try:
                                self.stock_dict[eachcode].set_ohlc_min_from_naver()
                            except:
                                time.sleep(4)
                                print('==='*30)
                                print(' C O N N E C T I O N E R R O R')
                                print('==='*30)
                                self.stock_dict[eachcode].set_ohlc_min_from_naver()
                            self.stock_dict[eachcode].set_candle_five()
                            self.stock_dict[eachcode].fill_index()
                            msg = self.stock_dict[eachcode].check_status(logmode=1) # 현재는 출력만 하고 있지만, 본 함수에 alert 또는 매매로직을 구현하면됨
                            
                            if msg is not None:
                                self.send_message_telegram(msg)

                        print('\n')
                        print(datetime.now()-st)
                        print('\n')
                        print('\n')
                        print('\n')
                        time.sleep(2)
            elif (marketready <= now < marketopen):

                print(' * INFO: MARKET READY, Current time : %s'%(now))
                time.sleep(60)

            else:

                print(' * INFO: MARKET CLOSED')
                break

    def send_message_telegram(self, message_dic='TEST'):
        '''

        탤래그램으로 메세지를 직접 보내는 함수

        :param message: dictionary
        :return:
        '''
        
        for k,v in message_dic.items():
            print(k, v)
        
        if self.RECEIVER and self.TOKEN:
            message = '%s (%s) : %s\nKDJ | %.3f / %.3f / %.3f\nBPW | %.3f / %.3f\nPMR | %.3f / %.3f / %.3f\nVMR | %.3f / %.3f / %.3f\n\nRULE: %s\nfinance.naver.com/item/main.nhn?code=%s'%(message_dic['STOCKNAME'],
                              message_dic['STOCKCODE'],
                              message_dic['TIME'],                                                                        
                              message_dic['K'],
                              message_dic['D'],
                              message_dic['J'],
                              message_dic['BBP'],      
                              message_dic['BBW'],
                              message_dic['PSMAR5'],
                              message_dic['PSMAR20'],
                              message_dic['PSMAR60'],
                              message_dic['VSMAR5'],
                              message_dic['VSMAR20'],
                              message_dic['VSMAR60'],
                              message_dic['COND_NAME'],
                              message_dic['STOCKCODE'])
                                                     

            
            self.BOT.sendMessage(self.RECEIVER, '%s' % (message))
        else:
            print(' * INFO: TELEGRAM TOKEN OR MESSAGE RECEIVER NOT SPECIFIED')
            
            
    def send_message_master(self):
        '''
        마스터 노드로 메세지를 보내는 함수, 미구현
        '''
        pass


if __name__ == '__main__':

    pass












