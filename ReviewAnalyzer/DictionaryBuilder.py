import FileManager
import NLP
import datetime
import os
import math
import main

reviewDic = None
wordDic = None
completeDic = None
baseDir = ''


def GetExistDic():
    global wordDic
    global completeDic
    global baseDir

    completeDic = []
    wordDic = []

    targetFileList = []
    fileList = os.listdir(baseDir + '\\Dic')
    for file in fileList:
        if file.__contains__('NormalWordDic'):
            targetFileList.append(baseDir + '\\Dic\\'+ file)

    if len(targetFileList) > 0:
        targetFileName = max(targetFileList)
        fileDes = open(targetFileName, 'r', encoding='utf-8')

        existData = FileManager.FileReader(fileDes)
        i = 0
        for data in existData:
            i += 1
            data = data[:len(data) - 1]
            dataList = data.split('#')
            dicData = []
            dicData.append(dataList[0])
            dicData.append(int(dataList[1]))
            dicData.append(dataList[2].split(','))

            wordDic.append(dicData)

    targetFileList = []
    fileList = os.listdir(baseDir + '\\Dic')
    for file in fileList:
        if file.__contains__('NormalCompleteList'):
            targetFileList.append(baseDir + '\\Dic\\'+ file)

    if len(targetFileList) > 0:
        targetFileName = max(targetFileList)
        readData = FileManager.FileReader(open(targetFileName, 'r', encoding='utf-8'))
        completeDic = readData[0].split(':')



def GetExistDicInfo():
    global wordDic
    GetExistDic()
    
    if len(wordDic) <= 0 or len(completeDic) <= 0:
        return None

    result = []
    result.append(wordDic)
    result.append(completeDic)

    return result


def BuildWordDic(workDir):
    global wordDic
    global reviewDic
    
    reviewDic = []

    GetExistDic()
    if wordDic == None:
        wordDic = []

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
        outPut += WordDicAppend(FileManager.FileReader(fileDes), file.split('.')[0], title, outPut)

    main.ShowTitle(title, outPut)
    wordDic = SortDic(wordDic, 0)
    return WriteDic()


def WordDicAppend(reviewData, fileName, title='', outPut=''):
    global wordDic

    skippedData = []
    index = 1
    dicWordList = []
    for dic in wordDic:
        dicWordList.append(dic[0])

    updateTime = int(str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))

    main.ShowTitle(title, outPut + 'Building dictionary for ' + fileName + ' (' + str(index) + '/' +  str(len(reviewData)) + ')')
    for data in reviewData:
        currentTime = int(str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
        if updateTime < currentTime:
            updateTime = currentTime
            main.ShowTitle(title, outPut + 'Building dictionary for ' + fileName + ' (' + str(index) + '/' +  str(len(reviewData)) + ')')

        splitData = data.split(',')
        if len(splitData) < 2:
            return 'No data in ' + fileName
            
        reviewNumber = fileName + '-' + splitData[0]
        if completeDic.__contains__(reviewNumber):
            skippedData.append(reviewNumber)
            continue

        splitData.remove(splitData[0])
        reviewString = ''.join(splitData)
        reviewString = reviewString.replace('\n', '')
        reviewString = reviewString.replace(';', ',')

        if reviewString == '!e':
            continue
        
        wordList = NLP.DoNLP(reviewString, 'None', 'Word')
        reviewDic.append(wordList)

        for word in wordList:
            if dicWordList.__contains__(word):
                targetIndex = dicWordList.index(word)
                wordDic[targetIndex][1] += 1
                sourceList = wordDic[targetIndex][2]
                if sourceList.__contains__(reviewNumber):
                    continue
                wordDic[targetIndex][2].append(reviewNumber)
                continue

            dicWordList.append(word)
            dicData = []
            dicData.append(word)
            dicData.append(1)
            sourceList = []
            sourceList.append(reviewNumber)
            dicData.append(sourceList)

            wordDic.append(dicData)

        index += 1
        completeDic.append(reviewNumber)

    returnString = "Complete building dictionary for " + fileName
    if len(skippedData) > 0:
        returnString += ' (skipped ' + str(len(skippedData)) + ' of ' + str(len(reviewData)) + ' review)'
    return returnString + '\n'


def SortDic(targetList, targetIndex, order='Ascend'):
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


def WriteDic():
    global baseDir
    global wordDic
    global completeDic

    timeStamp = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))

    if os.path.isdir(baseDir + '\\Dic') == False:
        os.makedirs(baseDir + '\\Dic')

    if os.path.isdir(baseDir + '\\Article\\Normal') == False:
        os.makedirs(baseDir + '\\Article\\Normal')

    fileName = timeStamp + '.txt'
    dataList = []
    for dic in reviewDic:
        sourceString = ';'.join(dic)
        dataList.append(sourceString)
    FileManager.FileWriter(baseDir + '\\Article\\Normal\\' + fileName, dataList, 'w')

    fileName = 'NormalWordDic-' + timeStamp + '.txt' 
    dataList = []
    for dic in wordDic:
        sourceString = ','.join(dic[2])
        data = dic[0] + '#' + str(dic[1]) + '#' + sourceString
        dataList.append(data)
    FileManager.FileWriter(baseDir + '\\Dic\\' + fileName, dataList, 'w')

    fileName = 'NormalCompleteList-' + timeStamp + '.txt'
    dataList = []
    data = ':'.join(completeDic)
    dataList.append(data)
    FileManager.FileWriter(baseDir + '\\Dic\\' + fileName, dataList, 'w')


def Proceed():
    if os.path.isdir('C:\\mecab') == False:
        return 'Please setup mecab NLP package before process'

    GetExistDic()

    targetDir = FileManager.DirSelector(baseDir)
    if targetDir == None:
        return ''

    return BuildWordDic(targetDir)


if __name__ == '__main__':
    baseDir = os.getcwd()

    targetDir = FileManager.DirSelector(baseDir)

    BuildWordDic(targetDir)
    wordDic = SortDic(wordDic, 0)
    WriteDic()