import os
import main

def FileReader(fileDes):
    readData = fileDes.readlines()

    fileDes.close()

    resultData = []
    for data in readData:
        resultData.append(data[:-1])
    
    return resultData


def FileWriter(fileName, dataList, mode='w'):
    fileName = RemoveInvaildChar(fileName)
    fileDes = open(fileName, mode, encoding='utf-8')

    for data in dataList:
        fileDes.write(data)
        fileDes.write('\n')

    fileDes.close()

def DirSelector(currentPath, outPut='', title=''):
    main.ShowTitle(currentPath + '\n' + outPut, title)

    fileList = os.listdir(currentPath)
    dirList = []
    dirList.append('..')
    
    for file in fileList:
        if len(file.split('.')) == 1:
            dirList.append(file)
            
    index = 0
    for dirName in dirList:
        print(str(index) + ": " + dirName)
        index += 1

    print('')
    print('y: Proceed')
    print('b: Quit selection')

    selectedDirIndexString = input("=> ")

    if selectedDirIndexString == 'y':
        return currentPath
    if selectedDirIndexString == 'b':
        return None

    try:
        selectedDirIndex = int(selectedDirIndexString)
    except:
        outPut = 'Please input a number'
        return DirSelector(currentPath)

    if selectedDirIndex >= index:
        outPut = 'Out of range'
    else:
        outPut = ''
        currentPath += '\\' + dirList[selectedDirIndex]

    return DirSelector(currentPath, outPut, title)

def RemoveInvaildChar(fileName, isDir=False):
    targetWordList = fileName.split('\\')
    extention = ''
    invaildChar = {"\\", "/", "'", '"', ":", "*", "?", "<", ">", "|", '.'}

    if isDir == False:
        extention = '.' + targetWordList[len(targetWordList) - 1].split('.')[1]

    for targetWord in targetWordList:
        index = targetWordList.index(targetWord)

        if index == 0:
            continue
        if index == len(targetWordList) - 1 and extention != '':
            targetWord = targetWord.split('.')[0]

        wordSet = set(targetWord)
        intersectedChar = wordSet & invaildChar

        if len(intersectedChar) > 0:
            for char in intersectedChar:
                if char == '.':
                    targetWord = targetWord.replace(char, '#')
                else:
                    targetWord = targetWord.replace(char, '')

        targetWordList[index] = targetWord

    fileName = '\\'.join(targetWordList) + extention

    if fileName[len(fileName) - 1] == ' ':
        fileName = fileName[:len(fileName) - 1]

    return fileName