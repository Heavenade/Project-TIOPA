import FileManager
import DataBaseManager
import ReviewDivider
import WordSimilarity
import NLP
import datetime
import os
import math
import main

baseDir = ''
insertQuery = []
updateQuery = []
similarWordDic = {}


def GetSimilarWordDic():
    global similarWordDic
    sqlResult = DataBaseManager.DoSQL("""
    SELECT  Sub_Word, Super_Word
    FROM    similar_word_dic
    """)

    if len(sqlResult) > 0:
        similarWordDic = dict(sqlResult)
    else:
        similarWordDic = {}


def BuildWordDic(workDir):
    fileList = os.listdir(workDir)
    targetFileList = []

    for file in fileList:
        nameSplit = file.split('.')
        if len(nameSplit) >= 2:
            if nameSplit[len(nameSplit) - 1] == 'txt':
                targetFileList.append(file)

    outPut = ''
    for file in targetFileList:
        try:
            fileDes = open(workDir + "\\" + file, 'r', encoding="utf-8")
        except:
            outPut += 'fail to open ' + file + '\n' + '\n'
            continue

        title = 'Now processing articles (' + str(targetFileList.index(file) + 1) + '/' + str(len(targetFileList)) + ')'
        outPut += AppendArticleDic(FileManager.FileReader(fileDes), file.split('.')[0], title, outPut)

    main.ShowTitle(title, outPut)

    WordSimilarity.baseDir = baseDir
    return WordSimilarity.ProcessArticle(outPut=outPut, title=None)


def GetSameStringIndex(data, targetString, prevIndexList=None):
    if prevIndexList == None:
        prevIndexList = []

    currentIndex = 0
    while True:
        if currentIndex >= len(data):
            break
        passing = False
        for indexList in prevIndexList:
            if currentIndex in indexList:
                passing = True
                break
        if passing:
            currentIndex += 1
            continue
        targetIndex = currentIndex + 1
        newTarget = [currentIndex]
        compareString = data[currentIndex].upper().replace(' ', '')
        while True:
            if targetIndex >= len(data):
                if compareString in targetString:
                    prevIndexList.append(newTarget)
                break
            passing = False
            for indexList in prevIndexList:
                if targetIndex in indexList:
                    passing = True
                    break
            if passing:
                break
            if (compareString + data[targetIndex].upper().replace(' ', '')) in targetString:
                newTarget.append(targetIndex)
                compareString += data[targetIndex].upper().replace(' ', '')
            else:
                if compareString in targetString:
                    prevIndexList.append(newTarget)
                    break
                else:
                    break
            targetIndex += 1
        currentIndex += 1
        
    return prevIndexList


def ConvertNormalWord(mainString=None, mainStringList=None, subString=None, subStringList=None, mode=None):
    global similarWordDic

    if subString == None:
        subString = ''
    if mode == None:
        mode = 'Word'

    # print('Do NLP', end='                                       \r')
    if mainString != None:
        mainStringList = NLP.DoNLP(mainString, None, mode)
    if subString != None:
        subStringList = NLP.DoNLP(subString, None, mode)

    wordList = []
    wordList.extend(mainStringList)
    if mainStringList != subStringList and len(subStringList) > 0:
        wordList.extend(subStringList)

    resultList = wordList

    # print('Get product', end='                                       \r')
    productDiscriptionList = ReviewDivider.GetProductName(' '.join(mainStringList), ' '.join(subStringList))

    if len(productDiscriptionList) > 0:
        resultList = []

        targetString = {}
        for discription, product in productDiscriptionList.items():
            if discription == 'product_Name':
                continue
            # print('Search ' + key + ' product in ' + str(len(wordList)) + ' words', end='                                       \r')
            targetStringIndex = GetSameStringIndex(wordList, discription)

            # print('Append fix dictionary', end='                                       \r')
            if len(targetStringIndex) > 0:
                existDic = targetString.get(product)
                if existDic == None:
                    existDic = []
                existDic.extend(targetStringIndex)
                newTarget = {product: existDic}
                targetString.update(newTarget)

        # print('Fixing string', end='                                       \r')
        removeTargetIndex = []
        insertedIndex = []
        for key, value in targetString.items():
            for indexList in value:
                modifiedWord = ''
                if indexList[0] in insertedIndex:
                    modifiedWord = wordList[indexList[0]] + 'ㅩ'
                else:
                    insertedIndex.append(indexList[0])
                wordList[indexList[0]] = modifiedWord + key

                for index in indexList:
                    if removeTargetIndex.__contains__(index) == False:
                        removeTargetIndex.append(index)

        # print('Make string', end='                                       \r')
        for i in range(len(wordList)):
            if removeTargetIndex.__contains__(i) == False:
                resultList.append(wordList[i])
            if i in insertedIndex:
                resultList.extend(wordList[i].split('ㅩ'))

    if mode == 'Review':
        wordList = resultList
        resultList = []
        for word in wordList:
            try:
                superWord = similarWordDic[word]
            except:
                resultList.append(word)
            else:
                resultList.append(superWord)

    return resultList


def AppendWordDicQuery(wordDic):
    global insertQuery
    global updateQuery

    stackUnit = DataBaseManager.maximumQueryStactUnit

    WordLastID = DataBaseManager.DoSQL("""
    SELECT `AUTO_INCREMENT`
    FROM  INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA = 'db_capstone'
    AND   TABLE_NAME   = 'similar_word_relation'""")[0][0]
    WordList = []
    index = 0
    while True:
        WordList.extend(DataBaseManager.DoSQL("""
        SELECT  Normal_Word, Similar_Relation_ID
        FROM    similar_word_relation
        WHERE   Similar_Relation_ID > """ + str(index) + """ AND Similar_Relation_ID <= """ + str(index + stackUnit)))
        index += stackUnit
        if index > WordLastID:
            break
    existWord = dict(WordList)

    for word, count in wordDic.items():
        try:
            RelationID = existWord[word]
        except:
            insertQuery.append("""
            INSERT INTO similar_word_relation (Normal_Word, Target_Word ,Word_Count)
            VALUES ('""" + word + """', '""" + word + """', """ + str(count) + """)
            """)
        else:
            updateQuery.append("""
            UPDATE  similar_word_relation
            SET     Word_Count = Word_Count + """ + str(count) + """
            WHERE   Similar_Relation_ID = """ + str(RelationID) + """
            """)


def AppendArticleDic(reviewData, fileName, title=None, outPut=None):
    global insertQuery
    global updateQuery

    if title == None:
        title = ''
    if outPut == None:
        outPut = ''

    insertQuery = []
    updateQuery = []
    stackUnit = DataBaseManager.maximumQueryStactUnit

    completeIndex = 0
    skippedIndex = 0
    
    articleLastID = DataBaseManager.DoSQL("""
    SELECT `AUTO_INCREMENT`
    FROM  INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA = 'db_capstone'
    AND   TABLE_NAME   = 'article_dic';
    """)[0][0]
    articleNumberList = []
    index = 0
    while True:
        articleNumberList.extend(DataBaseManager.DoSQL("""
        SELECT  Article_ID, Article_Number
        FROM    article_dic
        WHERE   Article_ID > """ + str(index) + """ AND Article_ID <= """ + str(index + stackUnit)))
        index += stackUnit
        if index > articleLastID:
            break
    completedReview = dict(articleNumberList)
    wordDic = {}

    main.ShowTitle(title, outPut + 'Building dictionary for ' + fileName + ' (' + str(completeIndex) + '/' +  str(len(reviewData)) + ')')
    updateTime = int(str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
    for data in reviewData:
        currentTime = int(str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
        if updateTime < currentTime:
            updateTime = currentTime
            main.ShowTitle(title, outPut + 'Building dictionary for ' + fileName + ' (' + str(completeIndex + skippedIndex) + '/' +  str(len(reviewData)) + ')')

        splitData = data.split(',')
        if len(splitData) < 2:
            return 'No data in ' + fileName

        reviewNumber = fileName + '-' + splitData.pop(0)
        reviewString = splitData.pop(0) + ','
        reviewString += ''.join(splitData)
        reviewString = reviewString.replace('\n', '')
        reviewString = reviewString.replace(';', ',')

        if reviewNumber in completedReview.values():
            skippedIndex += 1
            continue
        
        if reviewString == '!e':
            continue
        resultStringList = ConvertNormalWord(reviewString, reviewString)

        resultString = '#'.join(resultStringList)
        insertQuery.append("""
        INSERT INTO article_dic (Article_Number, Article)
        VALUES ('""" + reviewNumber + """', '""" + resultString + """')""")

        for word in resultStringList:
            try:
                currentCount = wordDic[word]
            except:
                currentCount = 0

            newItem = {word: currentCount + 1}
            wordDic.update(newItem)

        completeIndex += 1

    AppendWordDicQuery(wordDic)

    returnString = "Complete building dictionary for " + fileName
    if skippedIndex > 0:
        returnString += ' (skipped ' + str(skippedIndex) + ' of ' + str(len(reviewData)) + ' review)'
    returnString += '\n'

    DataBaseManager.DoManyQuery(insertQuery, title=title, outPut=outPut+returnString, queryType='INSERT')
    DataBaseManager.DoManyQuery(updateQuery, title=title, outPut=outPut+returnString, queryType='UPDATE')

    return returnString


def SortDic(targetList, targetIndex, order=None):
    if order == None:
        order = 'Ascend'

    if len(targetList) <= 1:
        return targetList

    pivot = targetList[len(targetList) // 2][targetIndex]
    lesserList, equalList, greaterList = [], [], []
    for num in targetList:
        if num[targetIndex] < pivot:
            lesserList.append(num)
        elif num[targetIndex] > pivot:
            greaterList.append(num)
        else:
            equalList.append(num)

    if order == 'Ascend':
        return SortDic(lesserList,targetIndex, order) + equalList + SortDic(greaterList,targetIndex, order)
    else:
        return SortDic(greaterList,targetIndex, order) + equalList + SortDic(lesserList,targetIndex, order)


def Proceed():
    if os.path.isdir('C:\\mecab') == False:
        return 'Please setup mecab NLP package before process'

    targetDir = FileManager.DirSelector(baseDir)
    if targetDir == None:
        return ''

    return BuildWordDic(targetDir)


if __name__ == '__main__':
    baseDir = os.getcwd()

    Proceed()