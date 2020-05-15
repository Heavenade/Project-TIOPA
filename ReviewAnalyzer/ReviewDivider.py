import FileManager
import NLP
import os
import datetime
import main

baseDir = ''
sourceName = ''
wordDic = []
absentDic = []
dividDic = []
productDic = []
completeReviewList = []


def Dividing(reviewData, fileName):
    global wordDic
    global absentDic
    global dividDic
    global productDic

    skippedData = []
    for data in reviewData:
        splitData = data.split(',')
        if len(splitData) < 2:
            return 'No data in ' + fileName

        reviewNumber = fileName + '-' + splitData[0]
        if completeReviewList.__contains__(reviewNumber):
            skippedData.append(reviewNumber)
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

        productMainDiscriptionList = []
        discriptedProductList = []
        productList = []
        for product in productDic:
            didGet = False
            for mainDiscription in product[4]:
                if mainDiscription == '':
                    continue
                if reviewTitleString.upper().replace(' ', '').__contains__(mainDiscription):
                    productMainDiscriptionList.append(mainDiscription)
                    discriptedProductList.append(product)
                    didGet = True
                    break

            if didGet:
                continue
            if len(productMainDiscriptionList) > 0:
                continue

            for subDiscription in product[5]:
                if subDiscription == '':
                    continue
                if reviewTitleString.upper().replace(' ', '').__contains__(subDiscription):
                    productList.append(product)
                    break            
        
        if len(productMainDiscriptionList) > 0:
            index = 0
            targetIndex = 0
            while True:
                if index >= len(productMainDiscriptionList):
                    break
                if targetIndex >= len(productMainDiscriptionList):
                    index += 1
                    targetIndex = 0
                    continue
                if index == targetIndex:
                    targetIndex += 1
                    continue
                
                if productMainDiscriptionList[index].__contains__(productMainDiscriptionList[targetIndex]):
                    productMainDiscriptionList.pop(targetIndex)
                    discriptedProductList.pop(targetIndex)
                else:
                    targetIndex += 1

            for product in discriptedProductList:
                resultList.append(product[0][0] + ' ' + product[1])

        else:
            if len(productList) > 0:
                for selectedProduct in productList:
                    isCorrect = False
                    for carrier in selectedProduct[0]:
                        if reviewString.upper().replace(' ', '').__contains__(carrier.upper().replace(' ', '')):
                            isCorrect = True
                            break
                    
                    if isCorrect:
                        resultList.append(selectedProduct[0][0] + ' ' + selectedProduct[1])
            
        
        if len(resultList) <= 0:
            resultList = NLP.DoNLP(reviewTitleString, 'NNP')

            nnpList = []
            for nnp in resultList:
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
            nnpList = []
            for nnp in resultList:
                if nnpList.__contains__(nnp) == False:
                    nnpList.append(nnp)

            for nnp in nnpList:
                existWord = False
                for word in wordDic:
                    if nnp == word[0]:
                        word[1].append(data)
                        existWord = True
                        break
                    
                if existWord:
                    continue

                newDic = []
                reviewList = []
                newDic.append(nnp)
                reviewList.append(data)
                newDic.append(reviewList)
                wordDic.append(newDic)

            for nnp in nnpList:
                existWord = False
                for word in dividDic:
                    if nnp == word[0]:
                        word[1] += 1
                        word[2].append(reviewNumber)
                        existWord = True
                        continue

                if existWord:
                    continue

                newDic = []
                reviewList = []
                newDic.append(nnp)
                newDic.append(1)
                reviewList.append(reviewNumber)
                newDic.append(reviewList)
                dividDic.append(newDic)


        completeReviewList.append(reviewNumber)

    returnString = "Complete building dictionary for " + fileName + '.'
    if len(skippedData) > 0:
        returnString += '(skipped ' + str(len(skippedData)) + ' of ' + str(len(reviewData)) + ' review)'
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
    main.ShowTitle('Now dividing reviews (0' + '/' + str(len(targetFileList)) + ')',outPut)
    for file in targetFileList:
        try:
            fileDes = open(workDir + "\\" + file, 'r', encoding="utf-8")
            outPut += Dividing(FileManager.FileReader(fileDes), file)
        except:
            failString += 'fail to open ' + workDir + "\\" + file + '\n'

        main.ShowTitle('Now dividing reviews (' + str(targetFileList.index(file) + 1) + '/' + str(len(targetFileList)) + ')', outPut)

    return WriteDic(FileManager.RemoveInvaildChar(baseDir + '\\Review\\' + sourceName, True))

    
def WriteDic(workDir):
    global sourceName
    global wordDic
    global productDic
    global absentDic

    if os.path.isdir(workDir) == False:
        os.makedirs(workDir)

    timeStamp = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    fileName = timeStamp + '.txt'

    for word in wordDic:
        DirName = FileManager.RemoveInvaildChar(workDir + '\\' + word[0], True)
        if os.path.isdir(DirName) == False:
            os.makedirs(DirName)

        reviewList = []
        for review in word[1]:
            reviewList.append(review)

        FileManager.FileWriter(DirName + '\\' + fileName, reviewList, 'a')
    
    if os.path.isdir(baseDir + '\\Dic') == False:
        os.makedirs(baseDir + '\\Dic')

    fileName = 'ProductList-' + timeStamp + '.txt' 

    currentCarrier = ''
    dataList = []
    for dic in productDic:
        data = ''
        if dic[0][0] != currentCarrier:
            for carrier in dic[0]:
                data = data + '%' + carrier
            currentCarrier = dic[0][0]
            dataList.append(data)

        data = dic[1] + '#' + dic[2] + '#' + str(dic[3]) + '#' + ','.join(dic[4]) + '#' + ','.join(dic[5])
        dataList.append(data)
        
    FileManager.FileWriter(baseDir + '\\Dic\\' + fileName, dataList, 'w')

    fileName = 'AbsentList-' + sourceName + '-' + timeStamp + '.txt'

    dataList = []
    for dic in absentDic:
        data = dic[0] + '#' + str(dic[1]) + '#' + ','.join(dic[2])
        dataList.append(data)

    FileManager.FileWriter(baseDir + '\\Dic\\' + fileName, dataList, 'w')

    fileName = 'DividList-' + sourceName + '-' + timeStamp + '.txt'

    dataList = []
    for dic in dividDic:
        data = dic[0] + '#' + str(dic[1]) + '#' + ','.join(dic[2])
        dataList.append(data)

    FileManager.FileWriter(baseDir + '\\Dic\\' + fileName, dataList, 'w')

    fileName = 'CompleteList-' + sourceName + '-' + timeStamp + '.txt'

    dataList = []
    data = ':'.join(completeReviewList)
    dataList.append(data)

    FileManager.FileWriter(baseDir + '\\Dic\\' + fileName, dataList, 'w')


def GetProductDic():
    global productDic
    global absentDic
    global dividDic
    global completeReviewList

    productDic = []
    absentDic = []
    dividDic = []
    completeReviewList = []

    targetFileList = []
    fileList = os.listdir(baseDir + '\\Dic')
    for file in fileList:
        if file.__contains__('ProductList'):
            targetFileList.append(baseDir + '\\Dic\\'+ file)

    if len(targetFileList) > 0:
        targetFileName = max(targetFileList)
        readData = FileManager.FileReader(open(targetFileName, 'r', encoding='utf-8'))
        productCarrier = []
        for data in readData:
            if data[0]  == '%':
                productCarrier = []
                data = data[1:]
                splitCarrier = data.split('%')
                for carrier in splitCarrier:
                    productCarrier.append(carrier)
                continue

            splitData = data.split('#')
            newProduct = []
            newProduct.append(productCarrier)
            productName = splitData[0]
            newProduct.append(productName)
            productCat = splitData[1]
            newProduct.append(productCat)
            productCount = int(splitData[2])
            newProduct.append(productCount)
            productMainDiscriptionList = splitData[3].split(',')
            newProduct.append(productMainDiscriptionList)
            productSubDiscriptionList = splitData[4].split(',')
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

    targetFileList = []
    fileList = os.listdir(baseDir + '\\Dic')
    for file in fileList:
        if file.__contains__('DividList'):
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

            dividDic.append(newDic) 

    targetFileList = []
    fileList = os.listdir(baseDir + '\\Dic')
    for file in fileList:
        if file.__contains__('CompleteList'):
            targetFileList.append(baseDir + '\\Dic\\'+ file)

    if len(targetFileList) > 0:
        targetFileName = max(targetFileList)
        readData = FileManager.FileReader(open(targetFileName, 'r', encoding='utf-8'))
        completeReviewList = readData[0].split(':')


def GetExistDicInfo():
    global productDic
    global absentDic
    global dividDic
    global completeReviewList

    GetProductDic()

    if len(completeReviewList) <= 0:
        return None
    
    result = []

    result.append(productDic)
    result.append(absentDic)
    result.append(dividDic)
    result.append(completeReviewList)

    return result


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