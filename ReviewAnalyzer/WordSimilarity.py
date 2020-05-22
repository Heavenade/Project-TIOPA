import main
import FileManager
import ReviewDivider
import DictionaryBuilder
import NLP
from gensim.models import FastText
import datetime
import os

contents = []
baseDir = ''
targetDir = ''
sourceName = ''
embedding_model = None


def SelectProduct(Mode, outPut='', title=''):
    global targetDir

    if Mode == 'Product':
        ReviewDivider.GetProductDic()
        if len(ReviewDivider.completeReviewList) <= 0:
            return 'There is no data'

        while True:
            main.ShowTitle(title, outPut)
            inputValue = input('Enter product Name (%q to back): ')

            if inputValue == '%q':
                return ''

            productList = ReviewDivider.GetProductName(inputValue)
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
                targetIndex = int(inputValue)
            except:
                outPut = 'Please enter correct number or charactor'
                continue

            if os.path.isdir(baseDir + '\\Review\\Product\\' + productList[targetIndex - 1]) == False:
                outPut = 'No review for ' + productList[targetIndex - 1]
                continue

            targetDir = baseDir + '\\Review\\Product\\' + productList[targetIndex - 1]
            GetSimilarity(title, GetContent(title))

            outPut = ''
            while True:
                main.ShowTitle('', outPut)
                inputValue = input('Enter target word (%q to back): ')

                if inputValue == '%q':
                    outPut = ''
                    break

                outPut = GetRelatedWord(inputValue)
    else:
        DictionaryBuilder.GetExistDic()
        if len(DictionaryBuilder.completeDic) <= 0:
            return 'There is no data'

        targetDir = baseDir + '\\Review\\Normal'
        GetSimilarity(title, GetContent(title))

        outPut = ''
        while True:
            main.ShowTitle('', outPut)
            inputValue = input('Enter target word (%q to back): ')

            if inputValue == '%q':
                outPut = ''
                break

            outPut = GetRelatedWord(inputValue)


def GetContent(title='', outPut=''):
    global contents
    global sourceName
    global targetDir

    sourceName = targetDir.split('\\')[len(targetDir.split('\\')) - 1]
    currentTime = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))

    targetArticleList = []
    targetFasttextList = []
    fileList = os.listdir(targetDir)
    for file in fileList:
        extension = file.split('.').pop()
        if extension == 'txt' and file.__contains__('Article-'):
            targetArticleList.append(file)
        if extension == 'fasttext':
            targetFasttextList.append(file)
    
    if len(targetFasttextList) > 0:
        if max(targetArticleList) > max(targetFasttextList):
            outPut = 'There is existing similarity data'
            return outPut

    for file in targetArticleList:
        readData = FileManager.FileReader(open(targetDir + '\\' + file, 'r', encoding='utf-8'))
        index = 0
        updateTime = int(str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
        main.ShowTitle(title, outPut + "Reading data from " + file + " (line " + str(index) + '/' + str(len(readData)) + ')')
        for data in readData:
            currentTime = int(str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
            if updateTime < currentTime:
                updateTime = currentTime
                main.ShowTitle(title, outPut + "Reading data from " + file + " (line " + str(index) + '/' + str(len(readData)) + ')')
            index += 1
            contents.append(data.split(';'))

        outPut += 'Complete reading data from ' + file + '\n'
        main.ShowTitle(title, outPut)

    return ''


def GetSimilarity(title='', outPut=''):
    global contents
    global baseDir
    global embedding_model
    global targetDir

    if outPut != '':
        main.ShowTitle(title, outPut)
        targetFileList = []
        fileList = os.listdir(targetDir)
        for file in fileList:
            extension = file.split('.').pop()
            if extension == 'fasttext':
                targetFileList.append(file)

        targetFileName = max(targetFileList)
        embedding_model = FastText.load(targetDir + '\\' + targetFileName)
    else:
        main.ShowTitle(title, 'Building similarity data')
        embedding_model = FastText(contents, size=100, window=5, min_count=5, workers=4, sg=1)
        currentTime = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        embedding_model.save(targetDir + '\\' + currentTime + '.fasttext')


def GetRelatedWord(word):
    global embedding_model
    global sourceName

    dataList = embedding_model.most_similar(positive=[word], topn=100)
    adjectiveList = []
    index = 0
    for data in dataList:
        if NLP.DoNLP(data[0], 'VA'):
            adjectiveList.append(dataList[index])
        index += 1

    outPut = '\n'
    outPut += "About '" + word + "' in " + sourceName + '\n'
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