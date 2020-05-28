import FileManager
import DataBaseManager
import DictionaryBuilder
import NLP
import os
import datetime
import math
import main

baseDir = ''
sourceName = ''
wordDic = []
absentDic = []
dividDic = []
productDic = []
completeReviewList = []


def SortProductList(targetIndex=1, order='Ascend'):
    carrierList = DictionaryBuilder.SortDic(GetProductCarrierList(0), 0, order)

    resultDic = []
    for carrier in carrierList:
        targetDic = []
        for dic in productDic:
            if dic[0][0] == carrier:
                targetDic.append(dic)
            
        resultDic.extend(DictionaryBuilder.SortDic(targetDic, targetIndex, order))

    return resultDic


def GetProductName(mainData='', subData=''):
    resultList = []
    if mainData == '':
        for dic in productDic:
            resultList.append(dic[1])

        return resultList

    productMainDiscriptionList = []
    discriptedProductList = []
    productList = []
    for product in productDic:
        didGet = False
        for mainDiscription in product[3]:
            if mainDiscription == '':
                continue
            if mainData.upper().replace(' ', '').__contains__(mainDiscription):
                productMainDiscriptionList.append(mainDiscription)
                discriptedProductList.append(product)
                didGet = True
                break

        if didGet:
            continue
        if len(productMainDiscriptionList) > 0:
            continue

        for subDiscription in product[4]:
            if subDiscription == '':
                continue
            if mainData.upper().replace(' ', '').__contains__(subDiscription):
                productList.append(product)
                break            
    
    if len(productMainDiscriptionList) > 0:
        discriptionIndex = 0
        targetIndex = 0
        while True:
            if discriptionIndex >= len(productMainDiscriptionList):
                break
            if targetIndex >= len(productMainDiscriptionList):
                discriptionIndex += 1
                targetIndex = 0
                continue
            if discriptionIndex == targetIndex:
                targetIndex += 1
                continue
            
            if productMainDiscriptionList[discriptionIndex].__contains__(productMainDiscriptionList[targetIndex]):
                productMainDiscriptionList.pop(targetIndex)
                discriptedProductList.pop(targetIndex)
            else:
                targetIndex += 1

        for product in discriptedProductList:
            resultList.append(product[1])
    else:
        if len(productList) > 0:
            for selectedProduct in productList:
                if subData != '':
                    isCorrect = False
                    for carrier in selectedProduct[0]:
                        if subData.upper().replace(' ', '').__contains__(carrier.upper().replace(' ', '')):
                            isCorrect = True
                            break
                else:
                    isCorrect = True
                
                if isCorrect:
                    resultList.append(selectedProduct[1])

    return resultList

def Dividing(reviewData, fileName, title='', outPut=''):
    global absentDic

    DataBaseManager.Connect()

    updateQuery = ''
    insertQuery = ''

    completeIndex = 0
    skippedIndex = 0
    updateTime = int(str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
    completedReview = []
    for data in DataBaseManager.DoSQL('SELECT Review_Number FROM review'):
        completedReview.append(data[0])

    main.ShowTitle(title, outPut + 'Building dictionary for ' + fileName + ' (' + str(completeIndex) + '/' +  str(len(reviewData)) + ')')
    for data in reviewData:
        currentTime = int(str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
        if updateTime < currentTime:
            updateTime = currentTime
            main.ShowTitle(title, outPut + 'Building dictionary for ' + fileName + ' (' + str(completeIndex + skippedIndex) + '/' +  str(len(reviewData)) + ')')

        splitData = data.split(',')
        if len(splitData) < 2:
            return 'No data in ' + fileName

        reviewNumber = fileName + '-' + splitData[0]
        if completedReview.__contains__(reviewNumber):
            skippedIndex += 1
            continue

        splitData.remove(splitData[0])
        reviewTitleString = splitData[0]
        splitData.remove(splitData[0])
        reviewString = ''.join(splitData)
        reviewString = reviewString.replace('\n', '')
        reviewString = reviewString.replace(';', ',')
        resultList = []

        if reviewTitleString == '!e':
            continue

        resultList = GetProductName(reviewTitleString, reviewString)
        
        if len(resultList) <= 0:
            wordList = NLP.DoNLP(reviewTitleString, 'NNP')

            nnpList = []
            for nnp in wordList:
                if nnpList.__contains__(nnp) == False:
                    nnpList.append(nnp)

            for nnp in nnpList:
                existWord = False
                for word in absentDic:
                    if nnp == word[0]:
                        word[1] += 1
                        word[2].append(reviewNumber)
                        existWord = True
                        break
                    
                if existWord:
                    continue

                newDic = []
                reviewList = []
                newDic.append(nnp)
                newDic.append(1)
                reviewList.append(reviewNumber)
                newDic.append(reviewList)
                absentDic.append(newDic)
        else:
            resultString = '#'.join(NLP.DoNLP(reviewString))
            for name in resultList:
                updateQuery += 'UPDATE product_dic SET Count = Count + 1 WHERE Name = "' + name + '";'
                productID = DataBaseManager.DoSQL('SELECT Product_ID FROM product_dic WHERE Name = "' + name + '"')[0][0]
                insertQuery += 'INSERT INTO review (Review_Number, Review, Product_ID) VALUES ("' + reviewNumber + '", "' + resultString + '", ' + str(productID) + ');'

        completeIndex += 1

    if updateQuery != '':
        DataBaseManager.DoSQL(updateQuery)
    if insertQuery != '':
        DataBaseManager.DoSQL(insertQuery)

    returnString = "Complete building dictionary for " + fileName
    if skippedIndex > 0:
        returnString += ' (skipped ' + str(skippedIndex) + ' of ' + str(len(reviewData)) + ' review)'
    return returnString + '\n'


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
            continue        
        
        outPut += Dividing(FileManager.FileReader(fileDes), file, title, outPut)

    return WriteDic()

    
def WriteDic(target=''):
    global baseDir
    global sourceName
    global wordDic
    global productDic
    global absentDic
    global completeReviewList

    timeStamp = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))

    # if target == 'Article' or target == '':
    #     if os.path.isdir(baseDir + '\\Article\\Product') == False:
    #         os.makedirs(baseDir + '\\Article\\Product')

    #     fileName = 'Article-' + timeStamp + '.txt'

    #     for word in wordDic:
    #         DirName = FileManager.RemoveInvaildChar(baseDir + '\\Article\\Product\\' + word[0], True)
    #         if os.path.isdir(DirName) == False:
    #             os.makedirs(DirName)

    #         dataList = []
    #         for review in word[1]:
    #             sourceString = ';'.join(review)
    #             dataList.append(sourceString)
    #         FileManager.FileWriter(DirName + '\\' + fileName, dataList, 'a')
    
    # if target == 'Product' or target == '':
    #     if os.path.isdir(baseDir + '\\Dic') == False:
    #         os.makedirs(baseDir + '\\Dic')

    #     fileName = 'ProductList-' + timeStamp + '.txt' 

    #     productDic = SortProductList()

    #     currentCarrier = ''
    #     dataList = []
    #     for dic in productDic:
    #         data = ''
    #         if dic[0][0] != currentCarrier:
    #             for carrier in dic[0]:
    #                 data = data + '%' + carrier
    #             currentCarrier = dic[0][0]
    #             dataList.append(data)

    #         data = dic[1] + '#' + dic[2] + '#' + ','.join(dic[3]) + '#' + ','.join(dic[4])
    #         dataList.append(data)
            
    #     FileManager.FileWriter(baseDir + '\\Dic\\' + fileName, dataList, 'w')

    if target == 'Absent' or target == '':
        if os.path.isdir(baseDir + '\\Dic') == False:
            os.makedirs(baseDir + '\\Dic')
        fileName = 'AbsentList-' + timeStamp + '.txt'

        dataList = []
        for dic in absentDic:
            data = dic[0] + '#' + str(dic[1]) + '#' + ','.join(dic[2])
            dataList.append(data)

        FileManager.FileWriter(baseDir + '\\Dic\\' + fileName, dataList, 'w')

    # if target == 'Divide' or target == '':
    #     fileName = 'DividList-' + timeStamp + '.txt'

    #     dataList = []
    #     for dic in dividDic:
    #         data = dic[0] + '#' + str(dic[1]) + '#' + ','.join(dic[2])
    #         dataList.append(data)

    #     FileManager.FileWriter(baseDir + '\\Dic\\' + fileName, dataList, 'w')

    # if target == 'Complete' or target == '':
    #     if os.path.isdir(baseDir + '\\Dic') == False:
    #         os.makedirs(baseDir + '\\Dic')
    #     fileName = 'ReviewCompleteList-' + timeStamp + '.txt'

    #     dataList = []
    #     data = ':'.join(completeReviewList)
    #     dataList.append(data)

    #     FileManager.FileWriter(baseDir + '\\Dic\\' + fileName, dataList, 'w')


def GetProductDic():
    global productDic
    global absentDic
    global dividDic
    global completeReviewList
    global sourceName

    productDic = []
    absentDic = []
    dividDic = []
    completeReviewList = []

    if os.path.isdir(baseDir + '\\Dic') == False:
        os.makedirs(baseDir + '\\Dic')
    DataBaseManager.Connect()

    productList = DataBaseManager.DoSQL('SELECT * FROM product_dic')
    for data in productList:
        productCarrier = []
        productMainDiscriptionList = []
        productSubDiscriptionList = []

        for result in DataBaseManager.DoSQL('SELECT Word FROM carrier_dic WHERE Carrier_ID = ' + str(data[3])):
            productCarrier.append(result[0])
        for result in DataBaseManager.DoSQL('SELECT Word FROM product_discription WHERE Product_ID = ' + str(data[0]) + ' AND Type = 1'):
            productMainDiscriptionList.append(result[0])
        for result in DataBaseManager.DoSQL('SELECT Word FROM product_discription WHERE Product_ID = ' + str(data[0]) + ' AND Type = 2'):
            productSubDiscriptionList.append(result[0])

        newProduct = []
        newProduct.append(productCarrier)
        newProduct.append(data[1])
        newProduct.append(data[2])
        newProduct.append(productMainDiscriptionList)
        newProduct.append(productSubDiscriptionList)

        productDic.append(newProduct)

    targetFileList = []
    fileList = os.listdir(baseDir + '\\Dic')
    for file in fileList:
        if file.__contains__('AbsentList'):
            targetFileList.append(baseDir + '\\Dic\\'+ file)

    if len(targetFileList) > 0:
        targetFileName = max(targetFileList)
        readData = FileManager.FileReader(open(targetFileName, 'r', encoding='utf-8'))
        for data in readData:
            splitData = data.split('#')
            newDic = []
            NNPName = splitData[0]
            newDic.append(NNPName)
            NNPCount = int(splitData[1])
            newDic.append(NNPCount)
            ReviewList = splitData[2].split(',')
            newDic.append(ReviewList)

            absentDic.append(newDic)

    # targetFileList = []
    # fileList = os.listdir(baseDir + '\\Dic')
    # for file in fileList:
    #     if file.__contains__('DividList'):
    #         targetFileList.append(baseDir + '\\Dic\\'+ file)

    # if len(targetFileList) > 0:
    #     targetFileName = max(targetFileList)
    #     readData = FileManager.FileReader(open(targetFileName, 'r', encoding='utf-8'))
    #     for data in readData:
    #         splitData = data.split('#')
    #         newDic = []
    #         NNPName = splitData[0]
    #         newDic.append(NNPName)
    #         NNPCount = int(splitData[1])
    #         newDic.append(NNPCount)
    #         ReviewList = splitData[2].split(',')
    #         newDic.append(ReviewList)

    #         dividDic.append(newDic) 

    # targetFileList = []
    # fileList = os.listdir(baseDir + '\\Dic')
    # for file in fileList:
    #     if file.__contains__('ReviewCompleteList'):
    #         targetFileList.append(baseDir + '\\Dic\\'+ file)

    # if len(targetFileList) > 0:
    #     targetFileName = max(targetFileList)
    #     readData = FileManager.FileReader(open(targetFileName, 'r', encoding='utf-8'))
    #     completeReviewList = readData[0].split(':')


def GetProductCategoryList():
    resultList = []

    for dic in productDic:
        if resultList.__contains__(dic[2]) == False:
            resultList.append(dic[2])

    return resultList


def GetProductCarrierList(targetIndex=0):
    resultList = []

    for dic in productDic:
        if targetIndex == -1:
            Carrier = dic[0]
        else:
            Carrier = dic[0][targetIndex]
        if resultList.__contains__(Carrier) == False:
            resultList.append(Carrier)

    return resultList


def ManageProduct(title='', outPut=''):
    GetProductDic()

    while True:
        main.ShowTitle(title, outPut)

        productName = input('Enter product name (%q to back): ')

        if productName == '%q':
            return ''

        while True:
            productList = GetProductName(productName)
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
                productPureName = productList[targetIndex - 1].split(' ')
                productPureName.pop(0)
                productPureName = ' '.join(productPureName)
                targetIndex = GetProductName().index(productPureName)
                while True:
                    main.ShowTitle(title, outPut)
                    print('1. Modify\n2. Delete')
                    modeInput = input('=> ')
                    
                    if modeInput == '1':
                        outPut = ''
                        outPutWork = 'Modify ' + productPureName
                        break
                    elif modeInput == '2':
                        ProductDictionaryRemove(targetIndex)
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
                dataList = []
                if i == 0:
                    dataList = GetProductCarrierList(-1)
                else:
                    dataList = GetProductCategoryList()
                while True:
                    main.ShowTitle(outPutWork + stateString[i] + '\n' + outPut, title)
                    number = 1
                    for propertyName in dataList:
                        print(str(number) + '. ', end='')
                        print(propertyName)
                        number += 1
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
                            propertyIndex = int(propertyInputValue)
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


def ProductDictionaryAppend(name, carrier, category, mainDiscriptionList, subDiscriptionList=[]):
    GetProductDic()

    newProduct = []
    newProduct.append(carrier)
    newProduct.append(name)
    newProduct.append(category)
    newProduct.append(mainDiscriptionList)
    newProduct.append(subDiscriptionList)

    productDic.append(newProduct)

    WriteDic('Product')


def ProductDictionaryModify(index, name='', carrier='', category='', mainDiscription=None, subDiscription=None):
    GetProductDic()

    targetDic = productDic[index]

    if carrier != '':
        targetDic[0] = carrier
    if name != '':
        targetDic[1] = name
    if category != '':
        targetDic[2] = category
    if mainDiscription != None:
        targetDic[3] = mainDiscription
    if subDiscription != None:
        targetDic[4] = subDiscription

    WriteDic('Product')


def ProductDictionaryRemove(index):
    GetProductDic()

    productDic.pop(index)

    WriteDic('Product')


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