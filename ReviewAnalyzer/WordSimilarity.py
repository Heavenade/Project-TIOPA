import main
import FileManager
import DataBaseManager
import ReviewDivider
import DictionaryBuilder
from BindSentiWords import  BindSentiWords
import NLP
from gensim.models import FastText
import datetime
import os
import math

contents = []
baseDir = ''
embedding_model = None


def ProcessAllProduct(outPut=None, title=None):
    global contents

    ReviewDivider.GetProductDic()
    productDic = ReviewDivider.productDic

    removeList = []
    for name, value in productDic.items():
        if value['RelationTable'] == None or value['Count'] <= 124:
            removeList.append(name)

    for name in removeList:
        productDic.pop(name)

    productDic = {k: v for k, v in sorted(productDic.items(), key=lambda item: item[1]['Count'], reverse=True)}

    index = 1
    for name, value in productDic.items():
        outPut = value['RelationTable'] + ' (' + str(index) + '/' + str(len(productDic)) + ')'
        GetContent(target=value['productID'], title=title, outPut=outPut)
        GetSimilarity(target=value['productID'], title=title, outPut=outPut)

        if len(contents) > 0:
            UpdateSimilarityDatabase(value['productID'], title=title, outPut=outPut)

        index += 1

    return ''


def ProcessArticle(outPut=None, title=None):
    global contents

    GetContent(target=None, outPut='Normal')
    GetSimilarity(target=None, title=title, outPut='Normal')

    if len(contents) > 0:
        UpdateSimilarityDatabase(target=None, title=title, outPut='Normal')
        UpdateSimilarWordDictionary(title=title, outPut='Normal')

    return ''


def SelectProduct(Mode, outPut=None, title=None):
    if title == None:
        title = ''
    if outPut == None:
        outPut = ''

    if Mode == 'Product':
        while True:
            main.ShowTitle(title, outPut)
            inputValue = input('Enter product Name (%q to back %a to process all): ')

            if inputValue == '%q':
                return ''

            if inputValue == '%a':
                return ProcessAllProduct()

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

            tableName = DataBaseManager.DoSQL("""
            SELECT  Relation_Table_Name
            FROM    product_dic
            WHERE   Product_ID = """ + str(targetID) + """
            LIMIT 1
            """)[0][0]
            if tableName == None:
                outPut = 'No review for ' + tableName
                continue
            
            GetContent(targetID, title=title, outPut=productList[int(inputValue)-1])
            GetSimilarity(targetID, title=title, outPut=productList[int(inputValue)-1])

            if len(contents) > 0:
                UpdateSimilarityDatabase(targetID, title=title, outPut=productList[int(inputValue)-1])

            outPut = ''
            while True:
                main.ShowTitle('', outPut)
                inputValue = input('Enter target word (%q to back): ')

                if inputValue == '%q':
                    outPut = ''
                    break

                outPut = GetRelatedWord(tableName, inputValue)
    else:
        articleCount = DataBaseManager.DoSQL("""
        SELECT  COUNT(*)
        FROM    article_dic
        """)[0][0]
        if articleCount <= 0:
            return 'There is no data'

        ProcessArticle()

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
        title = 'Get data for Analyze similarity'
    else:
        title += '\nGet data for Analyze similarity'
    if outPut == None:
        outPut = ''
    else:
        outPut = 'Process data of ' + outPut + '\n'
    
    targetDataList = []
    main.ShowTitle(title, outPut + "Find exist data")
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
        ORDER BY Review_ID DESC LIMIT 1
        """)
    lastUpdateDate = sqlResult[0][0]
    
    targetFasttextList = []
    if target == None:
        targetDir = baseDir + '\\WordVectorData\\Normal'
    else:
        targetDir = baseDir + '\\WordVectorData\\' + str(target)

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
    if title == None:
        title = 'Update Similar word Dictionary'
    else:
        title += '\nUpdate Similar word Dictionary'
    if outPut == None:
        outPut = ''
    else:
        outPut = 'Process data of ' + outPut + '\n'

    main.ShowTitle(title, 'Getting similarity data')
    sqlResult = DataBaseManager.DoSQL("""
    SELECT  Normal_Word, Target_Word, Word_Count
    FROM    similar_word_relation
    WHERE   Similar_Value > 0.95
    ORDER BY Similar_Value DESC
    """)

    index = 0
    wordDict = {}
    updateTime = 0
    for result in sqlResult:
        currentTime = int(str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
        if updateTime < currentTime:
            updateTime = currentTime
            main.ShowTitle(title, outPut + 'Building relation dictionary (' + str(index) + '/' + str(len(sqlResult)) + ')')
        newRelation = {result[1]: result[2]}
        try:
            existRelation = wordDict[result[0]]
        except:
            wordRelation = {result[0]: newRelation}
        else:
            existRelation.update(newRelation)
            wordRelation = {result[0]: existRelation}
        wordDict.update(wordRelation)
        index += 1

    index = 0
    removeIndex = 0
    initialLength = len(wordDict)
    removeList = []
    updateTime = 0
    for key, relation in wordDict.items():
        currentTime = int(str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
        if updateTime < currentTime:
            updateTime = currentTime
            main.ShowTitle(title, 'Removing unnecessary word (' + str(index) + '/' + str(initialLength) + ' removed: ' + str(removeIndex) + ')')
        if len(relation) <= 1:
            removeList.append(key)
            removeIndex += 1
        index += 1

    index = 0
    updateTime = 0
    for key in removeList:
        currentTime = int(str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
        if updateTime < currentTime:
            updateTime = currentTime
            main.ShowTitle(title, outPut + 'Removing unnecessary word (' + str(index) + '/' + str(initialLength) + ' removed: ' + str(removeIndex) + ')')
        wordDict.pop(key)

    relatedWordDict = {}
    SentiWordBinder = BindSentiWords.BindSentiWords()
    index = 0
    updateTime = 0
    for key, value in wordDict.items():
        currentTime = int(str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
        if updateTime < currentTime:
            updateTime = currentTime
            main.ShowTitle(title, outPut + 'Calculating sentimental value (' + str(index) + '/' + str(len(wordDict)) + ')')
        compareList = []
        compareList.extend(value.keys())
        sentiValueDict = SentiWordBinder.BindSentiWords(compareList)

        keySentiValue = sentiValueDict[key]
        if keySentiValue != 'None':
            sentiValueDict.pop(key)
            for word, targetSentiValue in sentiValueDict.items():
                if targetSentiValue != 'None':
                    if int(keySentiValue) == int(targetSentiValue):
                        if value[key] > wordDict[word][word]:
                            newRelation = {word: key}
                        elif value[key] < wordDict[word][word]:
                            newRelation = {key: word}
                        relatedWordDict.update(newRelation)

    index = 0
    updateTime = 0
    for subWord, superWord in relatedWordDict.items():
        currentTime = int(str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
        if updateTime < currentTime:
            updateTime = currentTime
            main.ShowTitle(title, outPut + 'Building similar word dictionary (' + str(index) + '/' + str(len(relatedWordDict)) + ')')
        try:
            upperWord = relatedWordDict[superWord]
        except:
            continue
        else:
            relatedWordDict[subWord] = upperWord
            for key, value in relatedWordDict.items():
                if value == superWord:
                    relatedWordDict[key] = upperWord

    main.ShowTitle(title, outPut + 'Getting exist similar word dictionary')
    sqlResult = DataBaseManager.DoSQL("""
    SELECT  Sub_Word, Similar_ID
    FROM    similar_word_dic
    """)
    existRelatedWordDict = dict(sqlResult)
    insertQuery = []
    updateQuery = []

    index = 0
    updateTime = 0
    for subWord, superWord in relatedWordDict.items():
        currentTime = int(str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
        if updateTime < currentTime:
            updateTime = currentTime
            main.ShowTitle(title, outPut + 'Appending Query (' + str(index) + '/' + str(len(relatedWordDict)) + ')')
        try:
            dictionaryID = existRelatedWordDict[subWord]
        except:
            insertQuery.append("""
            INSERT INTO similar_word_dic (Sub_Word, Super_Word)
            VALUES ('""" + subWord + """', '""" + superWord + """')
            """)
        else:
            updateQuery.append("""
            UPDATE  similar_word_dic
            SET     Super_Word
            WHERE   Similar_ID = """ + str(dictionaryID) + """
            """)

    DataBaseManager.DoManyQuery(insertQuery, title=title, outPut=outPut, queryType='INSERT')
    DataBaseManager.DoManyQuery(updateQuery, title=title, outPut=outPut, queryType='UPDATE')
    

def UpdateSimilarityDatabase(target=None, title=None, outPut=None):
    global embedding_model

    if title == None:
        title = 'Append Similar word relation'
    else:
        title += '\nAppend Similar word relation'
    if outPut == None:
        outPut = ''
    else:
        outPut = 'Process data of ' + outPut + '\n'

    main.ShowTitle(title, outPut + 'Getting exist data')

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
    else:
        sqlResult = DataBaseManager.DoSQL("""
        SELECT  Category_ID, Relation_Table_Name
        FROM    product_dic
        WHERE   Product_ID = """ + str(target) + """
        """)
        productInfo = sqlResult[0]

        featureList = [productInfo[1]]
        sqlResult = DataBaseManager.DoSQL("""
        SELECT  Feature_Name
        FROM    feature_dic
        WHERE   Category_ID = """ + str(productInfo[0]) + """
        """)
        for result in sqlResult:
            featureList.append(result[0])

    if target == None:
        main.ShowTitle(title, outPut + 'Getting latest calculated similar data')
        wordList = []
        for word in embedding_model.wv.index2word:
            wordList.append(word)

        wordDict = {}
        removeList = []
        index = 0
        updateTime = 0
        while True:
            currentTime = int(str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            if updateTime < currentTime:
                updateTime = currentTime
                main.ShowTitle(title, outPut + 'Removing not verb and adjective (' + str(index) + '/' + str(len(wordList)) + ' removed: ' + str(len(removeList)) + ')')
            word = wordList[index]
            targetTag = ['VA', 'VV']
            if len(NLP.DoNLP(word, targetTag)) <= 0:
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
    index = 0
    if target == None:
        updateTime = 0
        for word in wordDict.keys():
            result = embedding_model.most_similar(positive=[word], topn=len(embedding_model.wv.index2word) - 1)
            currentTime = int(str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            if updateTime < currentTime:
                updateTime = currentTime
                main.ShowTitle(title, outPut+'Append query (' + str(index) + '/' + str(len(wordList)) + ')')
            for similar in result:
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
    else:
        updateTime = 0
        for feature in featureList:
            result = embedding_model.most_similar(positive=[feature], topn=len(embedding_model.wv.index2word) - 1)
            currentTime = int(str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            if updateTime < currentTime:
                updateTime = currentTime
                main.ShowTitle(title, outPut + 'Append query (' + str(index) + '/' + str(len(featureList)) + ')')
            for similar in result:
                if feature != similar[0]:
                    # if feature != productInfo[1]:
                    #     try:
                    #         wordDict[similar[0]]
                    #     except:
                    #         updateQuery.append("""
                    #         UPDATE  `""" + productInfo[1] + """`
                    #         SET     `""" + feature + """` = null
                    #         WHERE   Word = '""" + similar[0] + """'
                    #         """)
                    #     else:
                    #         updateQuery.append("""
                    #         UPDATE  `""" + productInfo[1] + """`
                    #         SET     `""" + feature + """` = """ + str(similar[1]) + """
                    #         WHERE   Word = '""" + similar[0] + """'
                    #         """)
                    # else:
                    updateQuery.append("""
                    UPDATE  `""" + productInfo[1] + """`
                    SET     `""" + feature + """` = """ + str(similar[1]) + """
                    WHERE   Word = '""" + similar[0] + """'
                    """)

                    SentiWordBinder = BindSentiWords.BindSentiWords()
                    sentiValueDict = SentiWordBinder.BindSentiWords([similar[0]])
                    if sentiValueDict[similar[0]] != 'None':
                        updateQuery.append("""
                        UPDATE  `""" + productInfo[1] + """`
                        SET     Sentiment_Value = """ + sentiValueDict[similar[0]] + """
                        WHERE   Word = '""" + similar[0] + """'
                        """)

            updateQuery.append("""
            UPDATE  `""" + productInfo[1] + """`
            SET     `""" + feature + """` = null
            WHERE   Word_Count <= """ + str(5) + """
            """)

            index += 1

    if target == None:
        db = 'db_capstone'
    else:
        db = 'db_capstone_similarity'
        
    DataBaseManager.DoManyQuery(insertQuery, db=db, title=title, outPut=outPut, queryType='INSERT')
    DataBaseManager.DoManyQuery(updateQuery, db=db, title=title, outPut=outPut, queryType='UPDATE')

def GetSimilarity(target=None, title=None, outPut=None):
    global contents
    global baseDir
    global embedding_model

    if title == None:
        title = 'Building similarity data'
    else:
        title += '\nBuilding similarity data'
    if outPut == None:
        outPut = ''
    else:
        outPut = 'Process data of ' + outPut + '\n'

    currentTime = str(datetime.datetime.now().strftime('%Y#%m#%d&%H#%M#%S'))
    if target == None:
        saveDir = baseDir + '\\WordVectorData\\Normal\\' + currentTime + '.fasttext'
    else:
        saveDir = baseDir + '\\WordVectorData\\' + str(target) + '\\' + currentTime + '.fasttext'
    
    main.ShowTitle(title, outPut)
    if embedding_model == None:
        embedding_model = FastText(size=15, window=3, min_count=5, workers=4, sg=1)
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