import mysql.connector as mc
import config.config as cs
import pandas as pd
import time


ip = cs.IP
id = cs.ID
pw = cs.PW
dbScheme = cs.DBSCHEME



def insert(query):

    cnxn = mc.connect(host=ip, database=dbScheme, user=id, password=pw)
    cursor = cnxn.cursor()

    cursor.execute(query)
    # cursor.commit()
    cnxn.commit()
    cnxn.close()

def select(query):
    cnxn = mc.connect(host=ip, database=dbScheme, user=id, password=pw)
    cursor = cnxn.cursor()
    cursor.execute(query)
    table = cursor.fetchall()

    eachRow = []
    rtrlist = []
    for x in table:
        for y in list(x):
            eachRow.append(y)
        rtrlist.append(eachRow)
        eachRow = []

    cnxn.close()
    return rtrlist


def delete(query):
    cnxn = mc.connect(host=ip, database=dbScheme, user=id, password=pw)
    cursor = cnxn.cursor()
    cursor.execute(query,)

    cnxn.commit()
    cnxn.close()
    #return rtrlist



def selectInclueColumn(query):
    cnxn = mc.connect(host=ip, database=dbScheme, user=id, password=pw)
    cursor = cnxn.cursor()
    cursor.execute(query)
    table = cursor.fetchall()

    eachRow = []
    rtrlist = []
    for x in table:
        for y in list(x):
            eachRow.append(y)
        rtrlist.append(eachRow)
        eachRow = []

    cnxn.close()
    columns = [column[0] for column in cursor.description]
    return rtrlist,columns



def selectSingleValue(query):
    cnxn = mc.connect(host=ip, database=dbScheme, user=id, password=pw)
    cursor = cnxn.cursor()
    cursor.execute(query)
    table = cursor.fetchall()
    #print(type(table[0][0]))
    if(len(table) == 0):
        return None
    else:
        return table[0][0]


def selectSingleColumn(query):
    cnxn = mc.connect(host=ip, database=dbScheme, user=id, password=pw)
    cursor = cnxn.cursor()
    cursor.execute(query)
    table = cursor.fetchall()

    rtlist = []

    for eachRow in table:
        rtlist.append(eachRow[0])

    return rtlist



def selectpd(q):
    try:
        rs = selectInclueColumn(q)
        column = [str(col).replace('b', '').replace("'", '') for col in rs[1]]
        dt = rs[0]
        df = pd.DataFrame(data=dt, columns=column)
        return df

    except:

        time.sleep(3)
        rs = selectInclueColumn(q)
        column = [str(col).replace('b', '').replace("'", '') for col in rs[1]]
        dt = rs[0]
        df = pd.DataFrame(data=dt, columns=column)
        return df

def insertdf(df, table):


    templist = []
    for each in df.values.tolist():
        templist.append(tuple(each))
        # print(each)




    q = '''

    INSERT INTO %s
    VALUES %s''' % (table, str(tuple(templist))[1:-1])

    q= q.replace('nan','NULL')


    if q[-1]==',': q=q[:-1]

    try:
        insert(q.replace('nan','NULL'))
    except:
        time.sleep(0.4)
        try:
            insert(q)
        except Exception as e :
            print('ERROR! %s\n\t\t%s'%(e, q))
            pass
if(__name__ == '__main__'):

    query = 'SELECT * FROM jazzdb.T_STOCK_CODE_MGMT'
    print(selectpd(query))