import FileManager
import DataBaseManager
import DictionaryBuilder
import WordSimilarity
import NLP
import os
import datetime
import math
import main

baseDir = ''
sourceName = ''
productDic = {}
productSimilarDic = {}
similarInsertQuery = []
similarUpdateQuery = []
insertQuery = []
updateQuery = []


def SortProductList(targetIndex=None, order=None):
    if targetIndex == None:
        targetIndex = 1
    if order == None:
        order = 'Ascend'

    carrierList = DictionaryBuilder.SortDic(GetProductCarrierList(0), 0, order)

    resultDic = []
    for carrier in carrierList:
        targetDic = []
        for dic in productDic:
            if dic[0][0] == carrier:
                targetDic.append(dic)
            
        resultDic.extend(DictionaryBuilder.SortDic(targetDic, targetIndex, order))

    return resultDic


def GetProductName(mainData=None, subData=None):
    if mainData == None:
        mainData = ''
    if subData == None:
        subData = ''

    GetProductDic()

    resultDict = {'product_Name': []}
    if mainData == '':
        for product in productDic.keys():
            productList = resultDict.get('product_Name')
            productList.append(product)
            resultDict.update({'product_Name': productList})

        return resultDict

    productDiscriptionList = [{}, {}]
    discriptedProductList = {}
    for key, value in productDic.items():
        didGet = False
        for mainDiscription in value['mainDiscription']:
            if mainDiscription == '':
                continue
            if mainData.upper().replace(' ', '').__contains__(mainDiscription):
                wordList = mainData.split(' ')
                if len(DictionaryBuilder.GetSameStringIndex(wordList, mainDiscription)) > 0:    
                    newDiscription = {mainDiscription: key}
                    productDiscriptionList[0].update(newDiscription)
                    didGet = True
                    break
                for carrier in value['Carrier']:
                    if len(DictionaryBuilder.GetSameStringIndex(wordList, carrier.upper().replace(' ', '')+mainDiscription)) > 0:
                        newDiscription = {carrier.upper().replace(' ', '')+mainDiscription: key}
                        productDiscriptionList[0].update(newDiscription)
                        didGet = True
                        break
                break

        if didGet:
            continue
        if len(productDiscriptionList[0]) > 0:
            continue

        if subData != '':
            for subDiscription in value['subDiscription']:
                if subDiscription == '':
                    continue
                if mainData.upper().replace(' ', '').__contains__(subDiscription):
                    wordList = mainData.split(' ')
                    if len(DictionaryBuilder.GetSameStringIndex(wordList, subDiscription)) > 0:
                        targetProduct = discriptedProductList.get(subDiscription)
                        if targetProduct != None:
                            targetProduct = max(targetProduct, key)
                        else:
                            targetProduct = key
                        newDiscription = {subDiscription: targetProduct}
                        productDiscriptionList[1].update(newDiscription)
                    break
    
    for discriptionDict in productDiscriptionList:
        if len(discriptionDict) > 0:
            removeList = []
            for key in discriptionDict.keys():
                if key in removeList:
                    continue
                for targetKey in discriptionDict.keys():
                    if targetKey in removeList:
                        continue
                    if targetKey == key:
                        continue
                    if targetKey in key:
                        removeList.append(targetKey)
            for key in removeList:
                discriptionDict.pop(key)
    
    if len(productDiscriptionList[0]) > 0:
        resultDict.update(productDiscriptionList[0])
        for product in productDiscriptionList[0].values():
            productList = resultDict.get('product_Name')
            if product not in productList:
                productList.append(product)
                resultDict.update({'product_Name': productList})

    if len(productDiscriptionList[1]) > 0:
        if subData != '':
            for key, value in productDiscriptionList[1].items():
                isCorrect = False
                for carrier in productDic.get(value).get('carrier'):
                    if carrier.upper().replace(' ', '') in subData.upper().replace(' ', ''):
                        wordList = subData.split(' ')
                        if len(DictionaryBuilder.GetSameStringIndex(wordList, carrier.upper().replace(' ', ''))) > 0:
                            isCorrect = True
                        break
                    else:
                        break
            
                if isCorrect:
                    resultDict.update(productDiscriptionList[1])
                    for product in productDiscriptionList[1].values():
                        productList = resultDict.get('product_Name')
                        if product not in productList:
                            productList.append(product)
                            resultDict.update({'product_Name': productList})

    return resultDict


def AppendWordDicQuery(title=None, outPut=None):
    global productDic
    global productSimilarDic
    global similarInsertQuery
    global similarUpdateQuery
    global insertQuery
    global updateQuery

    if title == None:
        title = ''
    if outPut == None:
        outPut = ''

    featureDic = {}
    sqlResult = DataBaseManager.DoSQL("""
    SELECT  Feature_Name, Category_ID
    FROM    feature_dic
    """)

    for result in sqlResult:
        try:
            existFeatureList = featureDic[result[1]]
        except:
            existFeatureList = []
        
        existFeatureList.append(result[0])
        newDict = {result[1]: existFeatureList}
        featureDic.update(newDict)

    createQuery = []
    updateRelateTableQuery = []
    for name, wordDict in productSimilarDic.items():
        if productDic[name]['RelationTable'] == None:
            try:
                featureList = [name]
                featureList[1:] = featureDic[productDic[name]['categoryID']]
            except:
                featureList = [name]

            createQuery.append("""
            CREATE TABLE        `db_capstone_similarity`.`""" + name + """` (
                `Word_ID`       INT(11) NOT NULL AUTO_INCREMENT,
                `Word`          TEXT    NOT NULL,
                `Word_Count`    INT(11) NOT NULL DEFAULT '0',`""" + 
                '`FLOAT NULL DEFAULT NULL,`'.join(featureList)
                + """`          FLOAT NULL DEFAULT NULL,
                PRIMARY KEY (`Word_ID`)
            ) ENGINE = InnoDB
            """)

            updateRelateTableQuery.append("""
            UPDATE  product_dic
            SET     Relation_Table_Name = '""" + name + """'
            WHERE   Product_ID = """ + str(productDic[name]['productID']) + """
            """)

            productDic[name]['RelationTable'] = name
            existWord = {}
        else:
            WordList = []
            WordList.extend(DataBaseManager.DoSQL("""
            SELECT  `Word`, `Word_ID`
            FROM    `""" + name + """`""", 'db_capstone_similarity'))
            existWord = dict(WordList)

        for word, count in wordDict.items():
            try:
                wordID = existWord[word]
            except:
                similarInsertQuery.append("""
                INSERT INTO `""" + name + """` (`Word` ,`Word_Count`)
                VALUES ('""" + word + """', """ + str(count) + """)
                """)
            else:
                similarUpdateQuery.append("""
                UPDATE  `""" + name + """`
                SET     `Word_Count` = `Word_Count` + """ + str(count) + """
                WHERE   `Word_ID` = """ + str(wordID) + """
                """)

    DataBaseManager.DoManyQuery(createQuery, title=title, outPut=outPut, queryType='CREATE')
    DataBaseManager.DoManyQuery(updateRelateTableQuery, title=title, outPut=outPut, queryType='UPDATE')

def Dividing(reviewData, fileName, title=None, outPut=None):
    global similarInsertQuery
    global similarUpdateQuery
    global insertQuery
    global updateQuery

    if title == None:
        title = ''
    if outPut == None:
        outPut = ''

    similarInsertQuery = []
    similarUpdateQuery = []
    insertQuery = []
    updateQuery = []

    completeIndex = 0
    noProductIndex = 0
    skippedIndex = 0

    stackUnit = DataBaseManager.maximumQueryStactUnit

    articleLastID = DataBaseManager.DoSQL("""
    SELECT `AUTO_INCREMENT`
    FROM  INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA = 'db_capstone'
    AND   TABLE_NAME   = 'review_dic';
    """)[0][0]
    articleNumberList = []
    index = 0
    while True:
        articleNumberList.extend(DataBaseManager.DoSQL("""
        SELECT  Review_ID, Review_Number
        FROM    review_dic
        WHERE   Review_ID > """ + str(index) + """ AND Review_ID <= """ + str(index + stackUnit) + """
        """))
        index += stackUnit
        if index > articleLastID:
            break
    completedReview = dict(articleNumberList)

    updateTime = 0
    for data in reviewData:
        currentTime = int(str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
        if updateTime < currentTime:
            updateTime = currentTime
            main.ShowTitle(title, outPut + 'Building dictionary for ' + fileName + ' (' + str(completeIndex + skippedIndex) + '/' +  str(len(reviewData)) + ') (not product: ' + str(noProductIndex) + ')')

        splitData = data.split(',')
        if len(splitData) < 2:
            return 'No data in ' + fileName

        reviewNumber = fileName + '-' + splitData[0]
        splitData.remove(splitData[0])
        reviewTitleString = splitData[0]
        reviewTitleString = reviewTitleString.replace('\n', '')
        reviewTitleString = reviewTitleString.replace(';', ',')
        splitData.remove(splitData[0])
        reviewString = ''.join(splitData)
        reviewString = reviewString.replace('\n', '')
        reviewString = reviewString.replace(';', ',')

        if reviewNumber in completedReview.values():
            skippedIndex += 1
            continue

        if reviewTitleString == '!e':
            continue

        reviewTitleStringList = NLP.DoNLP(reviewTitleString, None, 'Review')
        reviewStringList = NLP.DoNLP(reviewString, None, 'Review')

        resultList = GetProductName(' '.join(reviewTitleStringList), ' '.join(reviewStringList)).get('product_Name')
        
        if len(resultList) > 0:
            resultStringList = DictionaryBuilder.ConvertNormalWord(mainStringList=reviewTitleStringList, subStringList=reviewStringList, mode='Review')
            resultString = '#'.join(resultStringList)

            for name in resultList:
                updateQuery.append("""
                UPDATE  product_dic
                SET     Count = Count + 1
                WHERE   Product_Name = '""" + name + """'
                """)
                insertQuery.append("""
                INSERT INTO review_dic (Review_Number, Review, Product_ID)
                VALUES ('""" + reviewNumber + """', '""" + resultString + """', """ + str(productDic[name].get('productID')) + """)
                """)
            
                for word in resultStringList:
                    try:
                        wordDict = productSimilarDic[name]
                    except:
                        wordDict = {}
                        
                    try:
                        currentCount = wordDict[word]
                    except:
                        currentCount = 0

                    wordInfo = {word: currentCount + 1}
                    wordDict.update(wordInfo)
                    newItem = {name: wordDict}
                    productSimilarDic.update(newItem)

            completeIndex += 1
        else:
            noProductIndex += 1

    returnString = "Complete building dictionary for " + fileName
    if skippedIndex > 0 or noProductIndex > 0:
        if skippedIndex > 0:
            returnString += ' (skipped: ' + str(skippedIndex)
        if noProductIndex > 0:
            returnString += ' / not product: ' + str(noProductIndex)
        returnString += ')'
    returnString += '\n'

    AppendWordDicQuery(title=title, outPut=outPut+returnString)
    DataBaseManager.DoManyQuery(insertQuery, title=title, outPut=outPut+returnString, queryType='INSERT')
    DataBaseManager.DoManyQuery(updateQuery, title=title, outPut=outPut+returnString, queryType='UPDATE')
    DataBaseManager.DoManyQuery(similarInsertQuery, 'db_capstone_similarity', title=title, outPut=outPut+returnString, queryType='INSERT')
    DataBaseManager.DoManyQuery(similarUpdateQuery, 'db_capstone_similarity', title=title, outPut=outPut+returnString, queryType='UPDATE')

    return returnString


def GetReviewData(workDir):
    global sourceName
    
    sourceName = workDir.split('\\')[len(workDir.split('\\')) - 1]
    fileList = os.listdir(workDir)
    targetFileList = []

    for file in fileList:
        nameSplit = file.split('.')
        if len(nameSplit) >= 2:
            if nameSplit[len(nameSplit) - 1] == 'txt':
                targetFileList.append(file)


    outPut = ''
    for file in targetFileList:
        title = 'Now dividing reviews (' + str(targetFileList.index(file) + 1) + '/' + str(len(targetFileList)) + ')'
        try:
            fileDes = open(workDir + "\\" + file, 'r', encoding="utf-8")
        except:
            outPut += 'fail to open ' + file + '\n' + '\n'
            main.ShowTitle(title, outPut)
        else:
            outPut += Dividing(FileManager.FileReader(fileDes), file, title, outPut)
            # DictionaryBuilder.AppendArticleDic(FileManager.FileReader(fileDes), file, title, outPut)
    
    WordSimilarity.baseDir = baseDir
    return WordSimilarity.ProcessAllProduct(title=None, outPut=outPut)


def GetProductDic(refresh=False):
    global productDic
    
    if refresh == True or len(productDic) <= 0:
        carrierAliasList = []
        productList = DataBaseManager.DoSQL("""
        SELECT  product_dic.Product_ID,
                product_dic.Carrier_ID,
                product_dic.Product_Name,
                product_dic.Category_ID,
                product_discription.Discription,
                product_discription.Type,
                product_dic.Count,
                product_dic.Relation_Table_Name
        FROM    product_dic
        LEFT JOIN product_discription
        ON product_dic.Product_ID = product_discription.Product_ID
        """)
        currentProductID = -1
        currentCarrierID = -1
        for data in productList:
            if data[1] != currentCarrierID:
                currentCarrierID = data[1]
                carrierAliasList = []
                sqlResult = DataBaseManager.DoSQL("""
                SELECT  Carrier_Alias
                FROM    carrier_dic
                WHERE   Carrier_ID = """ + str(currentCarrierID) + """
                """)
                for result in sqlResult:
                    carrierAliasList.append(result[0])
            if data[0] != currentProductID:
                currentProductID = data[0]
                newProduct = {'productID': data[0], 'categoryID': data[3], 'carrier': carrierAliasList, 'mainDiscription': [], 'subDiscription': [], 'Count': data[6], 'RelationTable': data[7]}
                newItem = {data[2]: newProduct}
                productDic.update(newItem)

            if data[5] == 1:
                productDic.get(data[2]).get('mainDiscription').append(data[4])
            elif data[5] == 2:
                productDic.get(data[2]).get('subDiscription').append(data[4])


def GetProductCategoryList():
    resultList = {}

    sqlResult = DataBaseManager.DoSQL("""
    SELECT Category_ID, Category
    FROM category_dic
    """)

    resultList = dict(sqlResult)

    return resultList


def GetProductCarrierList(targetID=0, getTitle=None, targetProduct=None):
    if getTitle == None:
        getTitle = False
    if targetProduct == None:
        targetProduct = ''

    resultList = {}

    if targetID == 0:
        if targetProduct == '':
            sqlResult = DataBaseManager.DoSQL("""
            SELECT Carrier_ID
            FROM product_carrier
            """)
        else:
            sqlResult = DataBaseManager.DoSQL("""
            SELECT Carrier_ID
            FROM product_carrier
            WHERE Carrier_Name = '""" + targetProduct + """'
            """)
        carrierList = []
        for result in sqlResult:
            carrierList.extend(result)

        if getTitle:
            for carrier in carrierList:
                sqlResult = DataBaseManager.DoSQL("""
                SELECT Carrier_Name
                FROM prodcut_carrier
                WHERE Carrier_ID = """ + str(carrier) + """
                """)
                newDic = {carrier: sqlResult[0][0]}
                resultList.update(newDic)
        else:
            for carrier in carrierList:
                sqlResult = DataBaseManager.DoSQL("""
                SELECT Carrier_Word_ID, Carrier_Alias
                FROM carrier_dic
                WHERE Carrier_ID = """ + str(carrier) + """
                """)
                aliasList = dict(sqlResult)
                newDic = {carrier: aliasList}
                resultList.update(newDic)
    else:
        sqlResult = DataBaseManager.DoSQL("""
        SELECT Carrier_ID, Carrier_Alias
        FROM carrier_dic
        WHERE Carrier_Word_ID = """ + str(targetID) + """
        """)
        newDic = {sqlResult[0][0]: {targetID: sqlResult[0][1]}}
        resultList.update(newDic)

    return resultList


def ManageProduct(title=None, outPut=None):
    if title == None:
        title = ''
    if outPut == None:
        outPut = ''

    GetProductDic()

    while True:
        main.ShowTitle(title, outPut)

        productName = input('Enter product name (%q to back): ')

        if productName == '%q':
            return ''

        while True:
            productList = GetProductName(productName).get('product_Name')
            main.ShowTitle('Data for ' + productName + '\n' + outPut, title)
            number = 1
            for product in productList:
                print(str(number) + '. Modify ' + product)
                number += 1
            print('')
            print('a. Add new product (' + productName + ')')
            print('r. Re-enter name')
            print('b. Back')
            inputValue = input('=> ')

            targetIndex = -1
            try:
                targetIndex = int(inputValue)
            except:
                if inputValue == 'r':
                    outPut = ''
                    break
                elif inputValue == 'b':
                    return ''
                elif inputValue == 'a':
                    outPut = ''
                    outPutWork = 'Add new product (' + productName + ')'
                else:
                    outPut = 'Please enter correct number or charactor'
                    continue

            if targetIndex != -1:
                productPureName = productList[targetIndex - 1]
                while True:
                    main.ShowTitle(title, outPut)
                    print('1. Modify\n2. Delete')
                    modeInput = input('=> ')
                    
                    if modeInput == '1':
                        outPut = ''
                        outPutWork = 'Modify ' + productPureName
                        break
                    elif modeInput == '2':
                        ProductDictionaryRemove(productPureName)
                        break

            outPutState = ''
            proceed = True
            name = ''
            propertyList = ['', []]
            DiscriptionList = []
            if inputValue != 'a':
                outPutState = '/ Name'
                main.ShowTitle(outPutWork + outPutState + '\n' + outPut, title)
                nameInputValue = input('Enter product name (%q to cancel add / %s to skip):')
                if nameInputValue == '%q':
                    proceed == False
                    outPut = ''
                elif nameInputValue == '%s':
                    name = ''
                    outPut = ''
                else:
                    name = nameInputValue
                    outPut = ''
            else:
                name = productName
                outPut = ''

            if proceed == False:
                continue

            for i in range(0, 2):
                stateString = [' / Carrier', ' / Category']
                targetString = ['carrier', 'category']
                if i == 0:
                    dataList = GetProductCarrierList(0)
                else:
                    dataList = GetProductCategoryList()
                while True:
                    main.ShowTitle(outPutWork + stateString[i] + '\n' + outPut, title)
                    for ID, propertyName in dataList.items():
                        print(str(ID) + '. ', end='')
                        print(propertyName)
                    print('')
                    if inputValue != 'a':
                        print('s. Skip')
                    if i == 1:
                        print('a. Add new ' + targetString[i])
                    print('b. Cancel add')
                    propertyInputValue = input('=> ')

                    if propertyInputValue == 'b':
                        proceed = False
                        outPut = ''
                        break
                    elif propertyInputValue == 's':
                        if inputValue != 'a':
                            propertyList[i] = ''
                            outPut = ''
                            break
                        else:
                            outPut = 'Please input without %'
                            continue
                    elif propertyInputValue == 'a':
                        if i == 0:
                            outPut = 'Please enter correct number or charactor'
                            continue
                        main.ShowTitle(outPutWork + outPutState + '\n' + outPut, title)
                        print('Enter' + targetString[i] + '!NO SPACE ENTER! (%q to cancel add', end='')
                        if inputValue != 'a':
                            print(' / %s to skip', end='')
                        propertyInputValue = input('): ')

                        if propertyInputValue == '%q':
                            outPut = ''
                            proceed = False
                            break
                        elif propertyInputValue == '%s':
                            if inputValue != 'a':
                                outPut = ''
                                propertyList[i] = ''
                                break
                            else:
                                outPut = 'Please input without %'
                                continue

                        propertyList[i] = propertyInputValue.replace(' ', '')
                    else:
                        try:
                            if propertyInputValue in dataList.keys():
                                propertyIndex = int(propertyInputValue)
                            else:
                                outPut = 'Please enter correct number or charactor'
                                continue
                        except:
                            outPut = 'Please enter correct number or charactor'
                            continue

                        propertyList[i] = dataList[propertyIndex - 1]
                        outPut = ''
                        break

                if proceed == False:
                    continue
                
            if proceed == False:
                continue

            for i in range(0,2):
                stateString = [' / Main discription', ' / Sub discription']
                targetString = ['main discription', 'sub discription']
                newList = []
                while True:
                    listString = ' data: ' + ', '.join(newList)
                    if inputValue != 'a':
                        listString += '(prev data: ' + ', '.join(productDic[targetIndex][i+3]) + ')'
                    main.ShowTitle(outPutWork + stateString[i] + listString + '\n' + outPut, title)
                    print('Enter ' + targetString[i] + ' !NO SPACE ENTER! (%q to cancel add / %f to finish add', end='')
                    if inputValue != 'a':
                        print(' / %s to skip', end='')
                    discriptionInputValue = input('): ')

                    if discriptionInputValue == '%q':
                        proceed == False
                        outPut = ''
                        break
                    elif discriptionInputValue == '%f':
                        outPut = ''
                        break
                    elif discriptionInputValue == '%s':
                        if inputValue != 'a':
                            newList = None
                            outPut = ''
                            break
                        else:
                            outPut = 'Please input without %'
                            continue
                    
                    newList.append(discriptionInputValue)
                    outPut = ''

                if proceed == False:
                    break

                DiscriptionList.append(newList)

            if proceed:
                if inputValue == 'a':
                    ProductDictionaryAppend(name, propertyList[0], propertyList[1], DiscriptionList[0], DiscriptionList[1])
                else:
                    ProductDictionaryModify(targetIndex, name, propertyList[0], propertyList[1], DiscriptionList[0], DiscriptionList[1])


def ProductDictionaryAppend(name, carrier, category, mainDiscriptionList, subDiscriptionList=None):
    dummy = ''

def ProductDictionaryModify(index, name=None, carrier=None, category=None, mainDiscription=None, subDiscription=None):
    dummy = ''

def ProductDictionaryRemove(index):
    dummy = ''

def Proceed():
    if os.path.isdir('C:\\mecab') == False:
        return 'Please setup mecab NLP package before process'

    GetProductDic()

    targetDir = FileManager.DirSelector(baseDir)
    if targetDir == None:
        return ''

    return GetReviewData(targetDir)


if __name__ == '__main__':
    baseDir = os.getcwd()

    Proceed()