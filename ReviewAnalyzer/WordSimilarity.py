import main
import FileManager
import DataBaseManager
import ReviewDivider
import DictionaryBuilder
import NLP
from gensim.models import FastText
import datetime
import os
import math

contents = []
baseDir = ''
embedding_model = None


def SelectProduct(Mode, outPut='', title=''):
    if Mode == 'Product':
        while True:
            main.ShowTitle(title, outPut)
            inputValue = input('Enter product Name (%q to back): ')

            if inputValue == '%q':
                return ''

            productList = ReviewDivider.GetProductName(inputValue).get('product_Name')
            main.ShowTitle(title, 'Data for ' + inputValue)
            number = 1
            if len(productList) > 0:
                for product in productList:
                    print(str(number) + '. ' + product)
                    number += 1
            else:
                print('No result')

            print('')
            print('r. Re-enter name')
            print('b. Back')

            inputValue = input("=> ")

            if inputValue == 'r':
                outPut=''
                continue
            elif inputValue == 'b':
                return ''
            
            try:
                sqlResult = DataBaseManager.DoSQL("""
                SELECT  Product_ID
                FROM    product_dic
                WHERE   Product_Name = '""" + productList[int(inputValue)-1] + """'
                """)[0]
                if sqlResult != []:
                    targetID = sqlResult[0]
                else:
                    outPut = 'Please enter correct number or charactor'
                    continue
            except:
                outPut = 'Please enter correct number or charactor'
                continue

            reviewList = DataBaseManager.DoSQL("""
            SELECT  *
            FROM    review_dic
            WHERE   Product_ID = """ + str(targetID) + """
            LIMIT 1
            """)
            if len(reviewList) <= 0:
                outPut = 'No review for ' + productList[int(inputValue)-1]
                continue

            GetSimilarity(targetID, title, GetContent(targetID, title))

            if len(contents) > 0:
                UpdateSimilarityDatabase(targetID)

            outPut = ''
            while True:
                main.ShowTitle('', outPut)
                inputValue = input('Enter target word (%q to back): ')

                if inputValue == '%q':
                    outPut = ''
                    break

                outPut = GetRelatedWord(productList[int(inputValue)-1], inputValue)
    else:
        articleList = DataBaseManager.DoSQL("""
        SELECT  *
        FROM    article_dic
        LIMIT 1
        """)
        if len(articleList) <= 0:
            return 'There is no data'

        GetSimilarity(None, title, GetContent(None, title))

        if len(contents) > 0:
            UpdateSimilarityDatabase(None)

        outPut = ''
        while True:
            main.ShowTitle('', outPut)
            inputValue = input('Enter target word (%q to back): ')

            if inputValue == '%q':
                outPut = ''
                break

            outPut = GetRelatedWord('Normal', inputValue)


def GetContent(target=None, title=None, outPut=None):
    global contents
    global embedding_model
    global baseDir
    
    if title == None:
        title = ''
    if outPut == None:
        outPut = ''
    
    targetDataList = []
    main.ShowTitle(title, outPut + "Reading data")
    if target == None:
        sqlResult = DataBaseManager.DoSQL("""
        SELECT  Date
        FROM    article_dic
        ORDER BY Article_ID DESC LIMIT 1
        """)
    else:
        sqlResult = DataBaseManager.DoSQL("""
        SELECT  Date
        FROM    review_dic
        WHERE   Product_ID = """ + str(target) + """
        ORDER BY Reivew_ID DESC LIMIT 1
        """)
    lastUpdateDate = sqlResult[0][0]
    
    targetFasttextList = []
    if target == None:
        targetDir = baseDir + '\\WordVectorData\\Normal'
    else:
        targetDir = baseDir + '\\WordVectorData\\' + target

    if os.path.isdir(targetDir):
        fileList = os.listdir(targetDir)
        for file in fileList:
            extension = file.split('.')[-1]
            fileName = '.'.join(file.split('.')[:-1])
            if extension == 'fasttext':
                targetFasttextList.append(fileName)
    else:
        os.makedirs(targetDir)
    
    lastProcessDate = '0000-00-00 00:00:00'
    if len(targetFasttextList) > 0:
        targetFileName = max(targetFasttextList)
        lastProcessDate = '-'.join(targetFileName.split('&')[0].split('#')) + ' ' + ':'.join(targetFileName.split('&')[1].split('#'))
        if targetFileName > lastUpdateDate.strftime('%Y#%m#%d&%H#%M#%S'):
            embedding_model = FastText.load(targetDir + '\\' + targetFileName + '.fasttext')
            outPut = 'There is existing similarity data'
    else:
        embedding_model = None

    targetDataList = []
    main.ShowTitle(title, outPut + "Reading data")
    if target == None:
        sqlResult = DataBaseManager.DoSQL("""
        SELECT  Article
        FROM    article_dic
        WHERE   Date > '""" + lastProcessDate + """' AND Article != ''
        """)
    else:
        sqlResult = DataBaseManager.DoSQL("""
        SELECT  Review
        FROM    review_dic
        WHERE   Date > '""" + lastProcessDate + """' AND Review != ''
        """)

    for result in sqlResult:
        if result != []:
            targetDataList.extend(result)

    for data in targetDataList:
        contents.append(data.split('#'))

    return ''


def UpdateSimilarWordDictionary(title=None, outPut=None):
    sqlResult = DataBaseManager.DoSQL("""
    SELECT  Normal_Word, Target_Word, Similar_Value, Word_Count
    FROM    simliar_word_relation
    WHERE   Similar_Value > 0.9
    ORDER BY Similar_Value DESC
    """)

    wordDict = {}
    for result in sqlResult:
        newRelation = {result[1]: [result[2], result[3]]}
        try:
            existRelation = wordDict[result[0]]
        except:
            wordRelation = {result[0]: newRelation}
        else:
            existRelation.update(newRelation)
        wordDict.update(newWord)


def UpdateSimilarityDatabase(target=None, title=None, outPut=None):
    global embedding_model

    if title == None:
        title = ''
    if outPut == None:
        outPut = ''

    main.ShowTitle(title, 'Appending Simliarity Database. Getting exist data')

    if target == None:
        relationDict = {}
        relationList = DataBaseManager.DoSQL("""
        SELECT  Normal_Word, Target_Word, Similar_Relation_ID
        FROM    similar_word_relation
        """)
        for relation in relationList:
            if relation[0] == relation[1]:
                newWordDict = {relation[0]: {}}
                relationDict.update(newWordDict)
            else:
                newRelation = {relation[1]: relation[2]}
                relationDict.get(relation[0]).update(newRelation)

    main.ShowTitle(title, 'Appending Simliarity Database. Getting latest calculated similar data')
    wordList = []
    for word in embedding_model.wv.index2word:
        wordList.append(word)
    wordDict = {}
    removeList = []
    index = 0
    main.ShowTitle(title, 'Appending Simliarity Database. Removing not verb and adjective (' + str(index) + '/' + str(len(wordList)) + ' removed: ' + str(len(removeList)) + ')')
    updateTime = int(str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
    while True:
        currentTime = int(str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
        if updateTime < currentTime:
            updateTime = currentTime
            main.ShowTitle(title, 'Appending Simliarity Database. Removing not verb and adjective (' + str(index) + '/' + str(len(wordList)) + ' removed: ' + str(len(removeList)) + ')')
        word = wordList[index]
        if len(NLP.DoNLP(word, ['VA', 'VV'])) <= 0:
            removeList.append(index)
        index += 1
        if index >= len(wordList):
            break

    removeList.sort(reverse=True)
    for index in removeList:
        wordList.pop(index)

    wordDict = dict.fromkeys(wordList)

    insertQuery = []
    updateQuery = []
    stackUnit = DataBaseManager.maximumQueryStactUnit
    index = 0
    for word in wordDict.keys():
        main.ShowTitle(title, 'Appending Simliarity Database. Calculating data of ' + word + ' (' + str(wordList.index(word)) + '/' + str(len(wordList)) + ')')
        result = embedding_model.most_similar(positive=[word], topn=len(embedding_model.wv.index2word) - 1)
        main.ShowTitle(title, 'Appending Simliarity Database. Append data of ' + word + ' (' + str(wordList.index(word)) + '/' + str(len(wordList)) + ')')
        for similar in result:
            if target == None:
                try:
                    wordDict[similar[0]]
                except:
                    continue
                else:
                    existData = relationDict.get(word)
                    try:
                        relationID = existData[similar[0]]
                    except:
                        newQuery = """
                        INSERT INTO similar_word_relation (Normal_Word, Target_Word, Similar_Value)
                        VALUES      ('""" + word + """', '""" + similar[0] + """', """ + str(similar[1]) + """)"""
                        insertQuery.append(newQuery)
                    else:
                        newQuery = """
                        UPDATE  similar_word_relation
                        SET     Similar_Value = """ + str(similar[1]) + """
                        WHERE   Similar_Relation_ID = """ + str(relationID)
                        updateQuery.append(newQuery)

                index += 1

    main.ShowTitle(title, 'Appending Simliarity Database. Finish appending data. Sending stacked query')
    if insertQuery != []:
        main.ShowTitle(title, 'Appending Simliarity Database. Sending INSERT query (' + str(0) + '/' + str(math.ceil(len(insertQuery) / stackUnit)) + ')')
        updateTime = int(str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
        for index in range(0, math.ceil(len(insertQuery) / stackUnit)):
            currentTime = 0
            if updateTime < currentTime:
                updateTime = currentTime
                main.ShowTitle(title, 'Appending Simliarity Database. Sending INSERT query (' + str(index) + '/' + str(math.ceil(len(insertQuery) / stackUnit)) + ')')
            Query = ';'.join(insertQuery[index*stackUnit:min(stackUnit*(index+1), len(insertQuery))])
            DataBaseManager.DoSQL(Query)
    if updateQuery != []:
        main.ShowTitle(title, 'Appending Simliarity Database. Sending INSERT query (' + str(0) + '/' + str(math.ceil(len(updateQuery) / stackUnit)) + ')')
        updateTime = 0
        for index in range(0, math.ceil(len(updateQuery) / stackUnit)):
            currentTime = int(str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            if updateTime < currentTime:
                updateTime = currentTime
                main.ShowTitle(title, 'Appending Simliarity Database. Sending INSERT query (' + str(index) + '/' + str(math.ceil(len(updateQuery) / stackUnit)) + ')')
            Query = ';'.join(updateQuery[index*stackUnit:min(stackUnit*(index+1), len(updateQuery))])
            DataBaseManager.DoSQL(Query)
        
    if insertQuery != []:
        Query = ';'.join(insertQuery)
        DataBaseManager.DoSQL(Query)
        insertQuery = []
    if updateQuery != []:
        updateQuery = ';'.join(updateQuery)
        DataBaseManager.DoSQL(updateQuery)
        updateQuery = []

def GetSimilarity(target=None, title=None, outPut=None):
    global contents
    global baseDir
    global embedding_model

    if title == None:
        title = ''
    if outPut == None:
        outPut = ''

    currentTime = str(datetime.datetime.now().strftime('%Y#%m#%d&%H#%M#%S'))
    if target == None:
        saveDir = baseDir + '\\WordVectorData\\Normal\\' + currentTime + '.fasttext'
    else:
        saveDir = baseDir + '\\WordVectorData\\' + str(target) + '\\' + currentTime + '.fasttext'
    
    main.ShowTitle(title, 'Building similarity data')
    if embedding_model == None:
        embedding_model = FastText(size=100, window=5, min_count=1, workers=4, sg=1)
        embedding_model.build_vocab(contents)
        embedding_model.train(contents, total_examples=embedding_model.corpus_count, epochs=embedding_model.epochs)
        embedding_model.save(saveDir)
    else:
        if len(contents) > 0:
            embedding_model.build_vocab(contents, update=True)
            embedding_model.train(contents, total_examples=embedding_model.corpus_count, epochs=embedding_model.epochs)
            embedding_model.save(saveDir)


def GetRelatedWord(sourceName, word):
    global embedding_model

    dataList = embedding_model.most_similar(positive=[word], topn=100)
    adjectiveList = []
    index = 0
    for data in dataList:
        if NLP.DoNLP(data[0], 'VA'):
            adjectiveList.append(dataList[index])
        index += 1

    outPut = '\n'
    outPut += "About '" + word + ' in ' + sourceName + '\n'
    outPut += 'Similar\t\t\t\tAjective\n'
    for i in range(0, 10):
        outPut += "{:10}\t".format(dataList[i][0])
        outPut += "{:1.4}\t\t".format(dataList[i][1])
        if i < len(adjectiveList):
            outPut += "{:10}\t".format(adjectiveList[i][0])
            outPut += "{:1.4}".format(adjectiveList[i][1])
        outPut += '\n'

    return outPut

def Proceed(Mode, title='', outPut=''):
    return SelectProduct(Mode, title, outPut)

if __name__ == '__main__':
    baseDir = os.getcwd()

    outPut = ''
    while True:
        main.ShowTitle(outPut)
        print('1. Product\n2. Normal word')
        inputValue = input('=> ')

        if inputValue == '1':
            outPut = Proceed('Product')
        elif inputValue == '2':
            outPut = Proceed('Normal')
        elif inputValue == 'q':
            exit()
        else:
            outPut = 'Please enter correct value or charactor\n'