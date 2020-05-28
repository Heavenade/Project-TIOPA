import pymysql
from pymysql.constants import CLIENT
connectedDB = None

def Connect():
    global connectedDB

    connectedDB = pymysql.connect(
        user='db_capstone',
        passwd='CapstoneWls.',
        host='db.p-cube.kr',
        db='db_capstone',
        charset='utf8',
        client_flag=CLIENT.MULTI_STATEMENTS
    )

    return connectedDB

def GetDB(db=None):
    global connectedDB

    if db == None:
        targetDB = connectedDB
    else:
        targetDB = db

    return targetDB

def DoSQL(query, db=None):
    targetDB = GetDB(db)
        
    cursor = targetDB.cursor()
    cursor.execute(query)
    targetDB.commit()
    result = [list(i) for i in cursor.fetchall()]

    if query.__contains__('INSERT INTO') or query.__contains__('UPDATE'):
        result = cursor.lastrowid

    return result

if __name__ == '__main__':
    Connect()
    query = 'SELECT Word FROM carrier_dic WHERE Carrier_ID = 1'
    # result = DoSQL("SELECT * FROM review")

    cursor = connectedDB.cursor()
    cursor.execute(query)
    connectedDB.commit()
    result = [list(i) for i in cursor.fetchall()]

    if query.__contains__('INSERT INTO'):
        result = cursor.lastrowid

    print(result)