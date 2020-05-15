import FileManager
import NLP
import os

wordDic = None
baseDir = ''


def GetExistDic():
    global wordDic
    global baseDir

    targetFileList = []
    fileList = os.listdir(baseDir + '\\Dic')
    for file in fileList:
        if file.__contains__('NormalWordDic'):
            targetFileList.append(baseDir + '\\Dic\\'+ file)

    if len(targetFileList) > 0:
        targetFileName = max(targetFileList)
        fileDes = open(targetFileName, 'r', encoding='utf-8')
    else:
        return

    wordDic = []

    existData = FileManager.FileReader(fileDes)
    i = 0
    for data in existData:
        print(i)
        i += 1
        data = data[:len(data) - 1]
        dataList = data.split(',')
        dicData = []
        dicData.append(dataList[0])
        dicData.append(int(dataList[1]))
        dicData.append(dataList[2].split(':'))

        wordDic.append(dicData)


def GetExistWord(word):
    global wordDic

    for dicData in wordDic:
        if dicData[0] == word:
            return wordDic.index(dicData)

    return -1


def GetExistDicInfo():
    global wordDic
    GetExistDic()
    if wordDic == None:
        return None

    result = []
    wordCount = 0
    reviewList = []
    for dic in wordDic:
        wordCount += dic[1]
        tmpReviewList = dic[2]
        for review in reviewList:
            while True:
                try:
                    tmpReviewList.pop(tmpReviewList.index(review))
                except:
                    break
        reviewList.extend(tmpReviewList)
        
    result.append(len(wordDic))
    result.append(wordCount)
    result.append(len(reviewList))

    return result


def BuildWordDic(workDir):
    global wordDic

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

    for file in targetFileList:
        try:
            fileDes = open(workDir + "\\" + file, 'r', encoding="utf-8")
        except:
            print('fail to open ' + workDir + "\\" + file)
            continue

        WordDicAppend(FileManager.FileReader(fileDes), file.split('.')[0])


def WordDicAppend(reviewData, sourceName):
    global wordDic

    for data in reviewData:
        splitData = data.split(',')
        if len(splitData) < 2:
            print('No data in ' + sourceName)
            return

        reviewNumber = sourceName + '-' + splitData[0]
        splitData.remove(splitData[0])
        reviewString = ''.join(splitData)

        if reviewString == '!e':
            continue
        
        wordList = NLP.DoNLP(reviewString)
        for word in wordList:
            dicIndex = GetExistWord(word)
            sourceList = []

            if dicIndex != -1:
                wordDic[dicIndex][1] +=  1
                sourceList = wordDic[dicIndex][2]
                sourceExist = False
                for sourceString in sourceList:
                    if sourceString == reviewNumber:
                        sourceExist = True
                        break
                if sourceExist == False:
                    wordDic[dicIndex][2].append(reviewNumber)
                continue

            dicData = []
            dicData.append(word)
            dicData.append(1)
            sourceList.append(reviewNumber)
            dicData.append(sourceList)

            wordDic.append(dicData)

    print("Complete building dictionary for " + sourceName)


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

    fileName = baseDir + '\\Dic'
    if os.path.isdir(fileName) == False:
        os.makedirs(fileName)

    fileName = fileName + '\\dic.txt'
    
    dataList = []
    index = 0
    for dic in wordDic:
        sourceString = ':'.join(dic[2])
        data = dic[0] + ',' + str(dic[1]) + ',' + sourceString
        dataList.append(data)
        index += 1
        
    FileManager.FileWriter(fileName, dataList)


if __name__ == '__main__':
    baseDir = os.getcwd()

    targetDir = FileManager.DirSelector(baseDir)

    BuildWordDic(targetDir)
    wordDic = SortDic(wordDic, 0)
    WriteDic()