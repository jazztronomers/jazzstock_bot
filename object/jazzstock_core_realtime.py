import pandas as pd
import time
import sys
import warnings
import config.config as cf
import config.condition as cd
import telepot
import jazzstock_bot
import os
import common.connector_db as db
from datetime import datetime
from object.jazzstock_object import JazzstockObject


pd.options.display.max_rows = 500
pd.options.display.max_columns= 500
warnings.filterwarnings('ignore')
timedf = pd.read_csv(os.path.join(jazzstock_bot.PATH_SRC_ROOT,'config/time.csv'), dtype=str)
tdic = {}
for tk, t1, t5, t15 in sorted(timedf.values.tolist()):
    tdic[str(tk).zfill(6)] = {'T1': str(t1).zfill(6), 'T5': str(t5).zfill(6), 'T15': str(t15).zfill(6)}

class JazzstockCoreRealtime:

    def __init__(self, stockcode_list, the_date, the_date_index, condition_dict=cd.COND_PROD):
        self.stock_dict = {}
        for stockcode in stockcode_list:
            self.stock_dict[stockcode] = JazzstockObject(stockcode, the_date=the_date, the_date_index=the_date_index, condition_dict = condition_dict)


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





class JazzstockCoreRealtimeNaver(JazzstockCoreRealtime):

    def __init__(self, stockcode_list=[], the_date = datetime.now().date(), the_date_index=0, condition_dict=cd.COND_PROD):
        super().__init__(stockcode_list, the_date, the_date_index, condition_dict)

        # OPTIONAL ==================================================================
        # NETWORK PARAMS, STANDALONE에서는 신경안써도됨
        self.MASTERIP = '127.0.0.1'
        # TELEGRAM ================================================
        self.TOKEN = cf.TELEBOT_TOKEN
        self.RECEIVER_SERVICE = cf.TELEBOT_ID
        self.RECEIVER_DEBUG = cf.TELEBOT_DEBUG
        self.BOT = telepot.Bot(self.TOKEN)
        # COMMON ==================================================
        self.THEDATE=the_date
        self.the_date_index=the_date_index
        self.queue = []


    def initialize_dataframe(self, cntto=0):
        '''
        초기화된 모든 종목에 대해서
        DB 특정거래일의 일봉정보와 분봉정보를 초기화하는 함수
        :return:
        '''

        listdf = pd.DataFrame()

        for eachcode in self.stock_dict.keys():
            try:
                self.stock_dict[eachcode].set_ohlc_min_from_db(cntto=cntto, window=20)
                self.stock_dict[eachcode].set_ohlc_day_from_db_include_index(cntto=cntto)
                self.stock_dict[eachcode].set_prev_day_index()
                listdf = listdf.append(self.stock_dict[eachcode].get_info())
            except:
                print('ERROR INITIALIZING - %s'%(eachcode))
                time.sleep(3)

        print('-'*100)
        print('전거래일 일봉기준 주가 및 지표 :')
        print(listdf.sort_values('BBP',ascending=True))
        print('-'*100)
        return listdf

    def debug(self, checktime=False, n=1):
        '''
        장종료후 디버깅목적함수
        최근거래일기준으로 개장후 2시간59분치 주가정보를 긁어옴
        '''

        import psutil
        import os
        import platform
        pid = os.getpid()
        platform_name = platform.system()


        print(' * RUN DEBUGGING ... PLATFORM: %s, PID: %s' %(platform_name, pid))
        self.initialize_dataframe(cntto=self.the_date_index+1)
        for j in ['09','10','11','12','13','14','15']: # 9시부터 9시 15분까지 1분단위로 디버깅
            for i in range(0, 60, n):
                ntime = '%s%s00' % (str(j).zfill(2), str(i).zfill(2))
                st =datetime.now()

                record = []
                for eachcode in self.stock_dict.keys():
                    # try:
                        elapesd_time_crawl = self.stock_dict[eachcode].set_ohlc_min_from_naver(is_debug=ntime, debug_date=self.stock_dict[eachcode].the_date)['elapsed_time']
                        elapesd_time_candle = self.stock_dict[eachcode].set_candle_five()['elapsed_time']
                        elapesd_time_calcindex = self.stock_dict[eachcode].fill_index()['elapsed_time']
                        ret = self.stock_dict[eachcode].check_status(
                            logmode=1)  # 현재는 출력만 하고 있지만, 본 함수에 alert 또는 매매로직을 구현하



                        elapesd_time_ifalert = ret['elapsed_time']
                        # if 'result' in ret.keys() and ret['result'] is not None:
                        #     self.send_message_telegram(ret['result'])
                        #     record.append(ret['result'])
                        #
                        meta = [float(x) for x in ret['meta']]

                        # ===================================================================================
                        # 성능모니터링용 BLOCK, 별 이슈없으므로 주석처리 # 2020-08-06
                        # ===================================================================================
                        # usage_cpu = round(psutil.cpu_percent() / psutil.cpu_count(),2)
                        # usage_mem_rss = round(psutil.Process(pid).memory_percent('rss'),3)
                        # usage_mem_vms = round(psutil.Process(pid).memory_percent('vms'),3)
                        # usage_mem_uss = round(psutil.Process(pid).memory_percent('uss'), 3)
                        #
                        # usage_list = [usage_cpu, usage_mem_rss, usage_mem_vms, usage_mem_uss]
                        # if platform_name=='Windows':
                        #     usage_list.append(round(psutil.Process(pid).memory_percent('wset'), 3))
                        # if platform_name=='Linux':
                        #     usage_list.append(round(psutil.Process(pid).memory_percent('pss'), 3))
                        #     usage_list.append(round(psutil.Process(pid).memory_percent('swap'), 3))
                        # ===================================================================================

                        print(eachcode, self.THEDATE, ntime, \
                              '%06d, C/V %d, %8d, | P | %+.3f\t%+.3f\t%+.3f\t | V | %+.3f\t%+.3f\t%+.3f\t\t%s'%tuple(meta))

                        self.db_queue(stockcode=eachcode, message_dic=ret['meta'])

                              # ,'\t', elapesd_time_crawl, elapesd_time_candle, elapesd_time_calcindex, elapesd_time_ifalert
                              # ,'\t', usage_list)


                    # except Exception as e:
                    #         print(" ** %s | ERROR: %s"%(eachcode, e))

                self.send_message_logging(record)
                self.db_insert(debug=True)

                if len(self.stock_dict) < 2:
                    time.sleep(0.02)
                else:
                    print(' * LEN : %s : %s' %(len(self.stock_dict.keys()),datetime.now()-st))
                    time.sleep(10) # 대책없이 긁으면 네이버에 막힐 수 있으므로, 한그룹 다돌면 10초씩 슬립하도록

    def run(self):
        '''
        WHILE LOOP 을 돌리면서, 1분마다 stock_dict을 looping하면서 분봉을 생성, 업데이트 하는 함수
        :return:
        '''
        marketready = datetime.strptime('08:40:00', '%H:%M:%S').time()
        marketopen = datetime.strptime('09:02:00', '%H:%M:%S').time()
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

                        record = []
                        for eachcode in self.stock_dict.keys():
                            try:
                                elapesd_time_d =self.stock_dict[eachcode].set_ohlc_min_from_naver()['elapsed_time']
                                elapesd_time_a = self.stock_dict[eachcode].set_candle_five()['elapsed_time']
                                elapesd_time_b = self.stock_dict[eachcode].fill_index()['elapsed_time']

                                temp = self.stock_dict[eachcode].check_status(logmode=1)# 현재는 출력만 하고 있지만, 본 함수에 alert 또는 매매로직을 구현하
                                
                                elapesd_time_c = temp['elapsed_time']
                                
                                if 'result' in temp.keys() and temp['result'] is not None:
                                    self.send_message_telegram(temp['result'])
                                    record.append(temp['result'])

                                print(eachcode, elapesd_time_d, elapesd_time_a, elapesd_time_b, elapesd_time_c)
                                self.db_queue(stockcode=eachcode, message_dic=temp['meta'])
                            except Exception as e:
                                time.sleep(1)
                                print('==='*30)
                                print(' * ERROR : %s, %s'%(eachcode, e))

                        self.db_insert()
                        self.send_message_logging(record)




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

        print(message_dic)
        # for k,v in message_dic.items():
        #     print(k, v)
        
        if self.RECEIVER_SERVICE and self.TOKEN:

            FLUCT = message_dic['CLOSE'] - self.stock_dict[message_dic['STOCKCODE']].dict_prev['01D_CLOSE']
            FLUCTRATIO = FLUCT / self.stock_dict[message_dic['STOCKCODE']].dict_prev['01D_CLOSE']

            if FLUCT >= 0:
                FLUCT = '+%s'%(FLUCT)
                FLUCTRATIO = '+%.2f%%'%(FLUCTRATIO*100)

            else:
                FLUCT = '%s' % (FLUCT)
                FLUCTRATIO = '%.2f%%' % (FLUCTRATIO * 100)

            message = '%s (%s) : %s / %s \n'%(message_dic['STOCKNAME'], message_dic['STOCKCODE'], message_dic['TIME'], message_dic['COND_NAME'])
            message = message + 'CLSE | %s (%s, %s)\n' % (message_dic['CLOSE'], FLUCT, FLUCTRATIO)
            message = message + 'PMAR | %.3f / %.3f / %.3f\n'%(message_dic['PSMAR5'],message_dic['PSMAR20'],message_dic['PSMAR60'])
            message = message + 'VMAR | %.3f / %.3f / %.3f\n'%(message_dic['VSMAR5'],message_dic['VSMAR20'],message_dic['VSMAR60'])
            message = message + 'BBPW | %.3f / %.3f\n\n'%(message_dic['BBP'], message_dic['BBW'])
            message = message + 'finance.naver.com/item/main.nhn?code=%s'%(message_dic['STOCKCODE'])

            self.BOT.sendMessage(self.RECEIVER_SERVICE, '%s' % (message))
        else:
            print(' * INFO: TELEGRAM TOKEN OR MESSAGE RECEIVER NOT SPECIFIED')

    def db_queue(self, stockcode, message_dic='TEST'):
        '''
        실시간 크롤링된 데이터를 DB에 INSERT 하는 함수
        개별종목마다 하만 안되고 모아서 한방에 해줘야함

        '''
        # print('DBQUEUE')

        # ['TIME', 'CLOSE', 'VOLUME', 'PSMAR5', 'PSMAR20', 'PSMAR60', 'VSMAR5', 'VSMAR20', 'VSMAR60', 'TRADINGVALUE']

        # AS-IS WITHOUT CLOSE, TRADINGVALUE, ONLY SMAR
        # message = [stockcode, str(self.THEDATE), message_dic[0], message_dic[3],message_dic[4],message_dic[5],message_dic[6],message_dic[7],message_dic[8]]

        # 20210327 CLOSE, TRADINGVALUE APPENDED
        message = [stockcode, str(self.THEDATE), message_dic[0], message_dic[3],message_dic[4],message_dic[5],message_dic[6],message_dic[7],message_dic[8], message_dic[1], message_dic[9],]
        self.queue.append(message)

    def db_insert(self, debug=False):
        '''
        '''


        if len(self.queue) > 0:
            rs = []
            for e in self.queue:
                rs.append(tuple(e[:-2] + [str(int(time.time())),0] + e[-2:]))  # 마지막은 AUTOINCREMENTS의 DUMMY VALUE

            query = 'INSERT INTO jazzdb.T_STOCK_MIN_05_SMAR_REALTIME VALUES %s' % (str(tuple(rs))[1:-2])
            if debug:
                print(query)
            else:
                db.insert(query)
            self.queue=[]
        else:
            print(' * debug: queue length is zero')

    def send_message_logging(self, record_list):
        '''

        :param record_list: 탤래그램으로 보낸 모든 메세지를 로그파일로 저장
        :return:
        '''
        f = open('record_%s.log' % (self.THEDATE), 'a')
        for each in record_list:
            f.write('%s\n'%(each))
        f.close()

if __name__ == '__main__':

    pass












