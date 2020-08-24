import common.connector_db as db
import argparse

class StockcodeManager():
    '''
    COMMAND LINE에서 ARGV를 받아서 쿼리를 실행하여 반환 받은 결과를
    BASH SCRIPT 로 SPACE SPLITED STRING (LIST) ARGV 넘겨야 할때 사용함
    '''
    def __init__(self, **params):

        self.query=''''''
        self.params_mandatory = self.parse_argv()

        for k,v in params.items():
            self.params_mandatory[k] = v


    def parse_argv(self):
        self.parser = argparse.ArgumentParser(description='Conditionally get Stockcode List')
        self.parser.add_argument('--row_num_from', type=int, default=0, metavar='f',
                            help='row_num_from')
        self.parser.add_argument('--row_num_to', type=int, default=20, metavar='t',
                            help='row_num_to')
        self.parser.add_argument('--date_idx', type=int, default=0, metavar='d',
                            help='date_idx')
        self.parser.add_argument('--verbose', type=int, default=0, metavar='v',
                            help="print query or not, 0 or 1")

        return vars(self.parser.parse_args())

    def set_query(self, query=None):

        print('HERE')
        if query is None:
            query = f'''
            SELECT STOCKCODE
            FROM
            (
                SELECT STOCKCODE,
                    ROW_NUMBER() OVER (PARTITION BY DATE ORDER BY I5 DESC) AS RN
                FROM jazzdb.T_STOCK_SND_ANALYSIS_RESULT_TEMP
                JOIN jazzdb.T_DATE_INDEXED USING (DATE)
                JOIN jazzdb.T_STOCK_MC USING (STOCKCODE, DATE)
                WHERE 1=1
                AND CNT = {self.params_mandatory['date_idx']}
                AND MC > 1          # 1300종목
            ) A
            WHERE 1=1
            AND RN BETWEEN {self.params_mandatory['row_num_from']} AND {self.params_mandatory['row_num_to']}
            '''
        return query

    def execute_query(self):
        df = db.selectpd(self.query)
        return list(df.STOCKCODE)

    def return_to_python(self):

        self.query = self.set_query()
        self.stockcode_list = self.execute_query()
        return self.stockcode_list

    def return_to_bash(self):
        self.stockcode_list = self.return_to_python()
        print(' '.join(self.stockcode_list))


class StockcodeManager_default(StockcodeManager):

    def __init__(self, **params):
        super().__init__(**params)
        self.params_mandatory = self.parse_argv()
        for k,v in params.items():
            self.params_mandatory[k] = v

    def parse_argv(self):

        super().parse_argv()
        self.parser.add_argument('--whom', type=str, default='ins', metavar='w',
                            help='window, option:ins, for, yg, samo')

        self.parser.add_argument('--window', type=int, default=5, metavar='n',
                            help='window, option:ins, for, yg, samo')

        self.parser.add_argument('--seperator', type=str, default='s', metavar='s',
                            help='s: space separated list, c: comma separated list,')

        self.parser.add_argument('--min_market_cap', type=int, default=1, metavar='m',
                            help='min_market_cap')

        self.parser.add_argument('--descending', type=str, default='DESC', metavar='m',
                            help='descending, DESC or ASC')

        return vars(self.parser.parse_args())

    def set_query(self, query=None):
        WINDOW_DICT = {

            'ins': 'I',
            'for': 'F',
            'yg': 'YG',
            'per': 'PS',
            'samo': 'S'

        }

        if query is None:
            query = f'''
            SELECT STOCKCODE
            FROM
            (
                SELECT STOCKCODE,
                    ROW_NUMBER() OVER (PARTITION BY DATE ORDER BY {WINDOW_DICT[self.params_mandatory['whom']]}{self.params_mandatory['window']} {self.params_mandatory['descending']}) AS RN
                FROM jazzdb.T_STOCK_SND_ANALYSIS_RESULT_TEMP
                JOIN jazzdb.T_DATE_INDEXED USING (DATE)
                JOIN jazzdb.T_STOCK_MC USING (STOCKCODE, DATE)
                WHERE 1=1
                AND CNT = {self.params_mandatory['date_idx']}
                AND MC > 1          # 1300종목
            ) A
            WHERE 1=1
            AND RN BETWEEN {self.params_mandatory['row_num_from']} AND {self.params_mandatory['row_num_to']}
            '''
        return query

class StockcodeManager_debug(StockcodeManager):
    '''

    DEBUGGING 목적 DATEIDX와 상관없이 고정된 STOCKCODELIST를 반환

    '''

    def return_to_python(self):
        return ['079940']

class StockcodeManager_rebound(StockcodeManager):

    def __init__(self,**params):
        super().__init__(**params)
        self.params_mandatory = self.parse_argv()
        for k,v in params.items():
            self.params_mandatory[k] = v


    # def parse_argv(self):
    #
    #     super().parse_argv()
    #     return vars(self.parser.parse_args())

    def set_query(self, query=None):
        query = f'''

            SELECT STOCKNAME, STOCKCODE, DATE, DATE_IDX, 
                    CURR_POS, 
                    FROM_PERIOD_HIGH, 
                    PERIOD_DIFF_MIN_MAX, 
                    DAYS_FROM_PERIOD_LOW, 
                    DAYS_FROM_PERIOD_HIGH
            FROM

            (
                SELECT STOCKCODE, DATE, DATE_IDX, OPEN, HIGH, LOW, CLOSE, 14D_MAX, 14D_MIN, RN_DATE,
                        # METADATA ==============================
                        RN_CLOSE, IS_MIN, IS_MAX, CURR_POS, FROM_PERIOD_HIGH, PERIOD_DIFF_MIN_MAX,
                        # METADATA ==============================
                        RN_MIN_DAY-RN_DATE AS DAYS_FROM_PERIOD_LOW,
                        RN_MAX_DAY-RN_DATE AS DAYS_FROM_PERIOD_HIGH
                FROM
                (
                    SELECT STOCKCODE, DATE, DATE_IDX, OPEN, HIGH, LOW, CLOSE, 14D_MAX, 14D_MIN, RN_DATE, RN_CLOSE, IS_MIN, IS_MAX, CURR_POS, FROM_PERIOD_HIGH, PERIOD_DIFF_MIN_MAX,
                            MAX(IS_MIN) OVER (PARTITION BY STOCKCODE) AS RN_MIN_DAY,
                            MAX(IS_MAX) OVER (PARTITION BY STOCKCODE) AS RN_MAX_DAY
                    FROM
                    (
                        SELECT STOCKCODE, DATE, DATE_IDX, OPEN, HIGH, LOW, CLOSE, 14D_MAX, 14D_MIN,
                            RN_DATE, RN_CLOSE,
                            CASE WHEN 14D_MIN=LOW THEN RN_DATE ELSE 0 END AS IS_MIN,
                            CASE WHEN 14D_MAX=HIGH THEN RN_DATE ELSE 0 END AS IS_MAX,
                            (CLOSE-14D_MIN)/(14D_MAX-14D_MIN) AS CURR_POS,       # 15거래일간 고점, 저점 대비 현주가의 위치
                            -(14D_MAX- CLOSE)/14D_MAX AS FROM_PERIOD_HIGH,       # 15거래일간 고점 대비 하락%
                            (14D_MAX- 14D_MIN)/14D_MAX AS PERIOD_DIFF_MIN_MAX    # 15거래일간 고점 대비 하락%

                        FROM
                        (
                            SELECT STOCKCODE, DATE, CNT AS DATE_IDX, OPEN, HIGH, LOW, CLOSE,
                                    MAX(HIGH) OVER (PARTITION BY STOCKCODE) AS 14D_MAX,
                                    MIN(LOW) OVER (PARTITION BY STOCKCODE) AS 14D_MIN,
                                    ROW_NUMBER() OVER (PARTITION BY STOCKCODE ORDER BY DATE DESC) AS RN_DATE,
                                    ROW_NUMBER() OVER (PARTITION BY STOCKCODE ORDER BY CLOSE DESC) AS RN_CLOSE

                            FROM
                            (
                                SELECT STOCKCODE, CNT, DATE, OPEN, HIGH, LOW, CLOSE
                                FROM jazzdb.T_STOCK_OHLC_DAY
                                JOIN jazzdb.T_DATE_INDEXED USING (DATE)
                                WHERE 1=1
                                # AND STOCKCODE = '278650'
                                AND CNT BETWEEN {self.params_mandatory['date_idx']} AND {self.params_mandatory['date_idx'] + 14}
                            ) A

                            WHERE 1=1
                            ORDER BY DATE DESC
                        ) B
                    ) C	
                )D
            ) E 
            JOIN jazzdb.T_STOCK_CODE_MGMT F USING (STOCKCODE)
            WHERE 1=1
            AND DAYS_FROM_PERIOD_LOW BETWEEN 2 AND 5				# 최저점에서 2일~ 5일 지난 종목
            AND DAYS_FROM_PERIOD_LOW < DAYS_FROM_PERIOD_HIGH		# 최저점이 최고점이후로 출연
            AND PERIOD_DIFF_MIN_MAX > 0.2 							# 15일간 최고점, 최저점 낙차가 20% 이상인 종목
            AND FROM_PERIOD_HIGH BETWEEN -0.2 AND -0.1				# 고점대비 10% ~ 20% 사이로 하락한 종목만
            AND CURR_POS BETWEEN 0.3 AND 0.5						# 전고점, 전저점 사이의 POSITION 이 0.3~ 0.5인 종목
            AND DATE_IDX ='{self.params_mandatory['date_idx']}'
            
            ORDER BY CURR_POS DESC
            LIMIT 30

            '''



        return query


if __name__ =='__main__':

    # COMMAND LINE 에서 실행시, RETURN 값을 출력해서
    # STDOUT parsing해서 값을 가져가기 위함

    obj = StockcodeManager()
    obj.return_to_bash()

    obj = StockcodeManager_default()
    obj.return_to_bash()

    obj = StockcodeManager_rebound()
    obj.return_to_bash()
    # stockcode_list=get_stockcode()
    # rt = SEPERATOR.join(stockcode_list)
    # print(rt)



