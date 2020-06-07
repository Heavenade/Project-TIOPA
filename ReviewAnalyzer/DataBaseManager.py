import pymysql
from pymysql.constants import CLIENT

maximumQueryStactUnit = 5000

def Connect():
    print('Database connecting', end='                      \r')

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
    if db == None:
        targetDB = Connect()
    else:
        targetDB = db

    return targetDB

def DoSQL(query, db=None):
    targetDB = GetDB(db)
    cursor = targetDB.cursor()
        
    print('Executing query', end='                      \r')
    cursor.execute(query)
    print('Fetching result', end='                      \r')
    result = [list(i) for i in cursor.fetchall()]
    print('Commiting result', end='                      \r')
    targetDB.commit()

    if query.__contains__('INSERT INTO') or query.__contains__('UPDATE'):
        result = cursor.lastrowid

    cursor.close()
    targetDB.close()
    print('Querying finish', end='                      \r')

    return result

if __name__ == '__main__':
    query = '''

    '''
    result = DoSQL(query)

    print(result)