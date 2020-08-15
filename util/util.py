import common.connector_db as db

def date_to_index(date):
    cnt = db.selectSingleValue("SELECT CNT FROM jazzdb.T_DATE_INDEXED WHERE 1=1 AND DATE = '%s'"%(date))
    return cnt

def index_to_date(idx):
    thedate = db.selectSingleValue("SELECT DATE FROM jazzdb.T_DATE_INDEXED WHERE 1=1 AND CNT = '%s'"%(idx))
    return thedate



