import main
import datetime
import math
import pymysql
from pymysql.constants import CLIENT

maximumQueryStactUnit = 10000

def Connect(dbName):
    print('Database connecting at ' + dbName , end='                                            \r')

    try:
        connectedDB = pymysql.connect(
            user='db_capstone',
            passwd='CapstoneWls.',
            host='db.p-cube.kr',
            db=dbName,
            charset='utf8',
            client_flag=CLIENT.MULTI_STATEMENTS
        )
    except Exception as err:
        print('Connection Error! (', end='')
        print(err, end='')
        print(')')

        return Connect(dbName)

    return connectedDB

def GetDB(db=None):
    if db == None:
        targetDB = Connect('db_capstone')
    else:
        targetDB = Connect(db)

    return targetDB

def DoSQL(query, db=None):
    targetDB = GetDB(db)
    cursor = targetDB.cursor()
        
    print('Executing query', end='                                            \r')
    cursor.execute(query)
    print('Fetching result', end='                                            \r')
    result = [list(i) for i in cursor.fetchall()]
    print('Commiting result', end='                                            \r')
    targetDB.commit()

    if query.__contains__('INSERT INTO') or query.__contains__('UPDATE'):
        result = cursor.lastrowid

    cursor.close()
    targetDB.close()
    print('Querying finish', end='                                            \r')

    return result

def DoManyQuery(queryList, db=None, title=None, outPut=None, queryType=None):
    if title == None:
        title = ''
    if outPut == None:
        outPut = ''
    if queryType == None:
        queryType = ''
        
    if queryList != []:
        updateTime = 0
        for index in range(0, math.ceil(len(queryList) / maximumQueryStactUnit)):
            currentTime = int(str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            if updateTime < currentTime:
                updateTime = currentTime
                main.ShowTitle(title, outPut + 'Sending ' + queryType + ' query (' + str(index) + '/' + str(math.ceil(len(queryList) / maximumQueryStactUnit)) + ')')
            Query = ';'.join(queryList[index*maximumQueryStactUnit:min(maximumQueryStactUnit*(index+1), len(queryList))])
            DoSQL(Query, db)

if __name__ == '__main__':
    query = '''
    SELECT  COUNT(*)
    FROM    article_dic
    '''
    result = DoSQL(query)

    print(result)