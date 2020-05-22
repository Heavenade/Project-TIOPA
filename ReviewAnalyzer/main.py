import os
import DictionaryBuilder
import ReviewDivider
import WordSimilarity

result = None

def ShowTitle(outPut='', currentPosition=''):
    os.system('cls')
    print('Typical Impression Analyzer for Product')
    print(currentPosition, end='')
    print('')
    print(outPut, end='')
    print('')

def ShowFrequentWord(limit, targetList, dataIndex=0, targetIndex=0, outPut='', title=''):
    sortedDic = DictionaryBuilder.SortDic(targetList, targetIndex, 'Descend')

    while True:
        ShowTitle(outPut, title)

        for index in range(0,limit):
            print(str(index + 1) + '. ' + str(sortedDic[index][dataIndex]) + ', ' + str(sortedDic[index][targetIndex]))

        print('')
        print('b. Return to Main menu')
        inputValue = input('=> ')

        if inputValue == 'b':
            return ''

        outPut = 'Please enter correct number or charactor\n'

def ShowSearchResult(targetList, targetIndex, printDataList, outPut='', title=''):
    while True:
        ShowTitle(outPut, title)

        inputValue = input("Enter word (%q to return): ")
        if inputValue == '':
            outPut = 'Please enter word'
            continue
        if inputValue == '%q':
            return ''
        targetData = inputValue

        targetDataList = []
        for data in targetList:
            targetDataList.append(data[targetIndex].upper().replace(' ', ''))

        resultIndex = -1
        if targetDataList.__contains__(targetData.upper().replace(' ','')):
            resultIndex = targetDataList.index(targetData.upper().replace(' ',''))

        printTitleList = []
        printIndexList = []
        for data in printDataList:
            printTitleList.append(data.split('#')[0])
            printIndexList.append(int(data.split('#')[1]))

        outPut = ''
        if resultIndex == -1:
            outPut = 'No result of ' + targetData
        else:
            outPut = targetData + "\t"
            for i in range(0, len(printTitleList)):
                outPut += printTitleList[i] + ": " + str(targetList[resultIndex][printIndexList[i]]) + '\t'

def NormalWordDictionaryMenu(outPut=''):
    result = DictionaryBuilder.GetExistDicInfo()
    if result != None:
        wordDic = result[0]
        completeDic = result[1]

        wordCount = 0
        for dic in wordDic:
            wordCount += dic[1]
    while True:
        number = 1
        if result == None:
            ShowTitle('No exist Normal word Dictionary\n' + outPut, 'Normal word Dictionary Menu\n')
        else:
            ShowTitle(outPut)
            print('words: ' + str(len(wordDic)) + ' / total words: ' + str(wordCount) + ' / reviews: ' + str(len(completeDic)))
            print(str(number) + '. Show 20 Most frequent words')
            number += 1
            print(str(number) + '. Search word')
            number += 1
            print(str(number) + '. Edit Representitive word')
            number += 1
        print(str(number) + '. Input new data')
        print('')
        print('b. Back')
        inputValue = input('=> ')

        if result == None:
            if inputValue == '1':
                outPut = DictionaryBuilder.Proceed()
                return NormalWordDictionaryMenu(outPut)
        else:
            if inputValue == '1':
                ShowFrequentWord(20, wordDic, 0, 1, '', '20 Most frequent words')
                continue
            elif inputValue == '2':
                ShowSearchResult(wordDic, 0, ['Count#1'], '', 'Search Normal word Dictionary')
                continue
            elif inputValue == '3':
                outPut = 'This feature is not ready\n'
                continue
            elif inputValue == '4':
                outPut = DictionaryBuilder.Proceed()
                return NormalWordDictionaryMenu(outPut)
            
        if inputValue == 'b':
            return ''
        else:
            outPut = 'Please enter correct number or charactor\n'
            continue

def ReviewDictionaryMenu(outPut=''):
    ReviewDivider.GetProductDic()
    noData = True
    if len(ReviewDivider.completeReviewList) > 0:
        noData = False
        productCount = 0
        wordCount = 0
        for dic in ReviewDivider.dividDic:
            productCount += dic[1]
        for dic in ReviewDivider.absentDic:
            wordCount += dic[1]
    
    while True:
        number = 1
        if noData:
            ShowTitle('No exist Review Dictionary\n' + outPut, 'Review Dictionary Menu\n')
        else:
            ShowTitle(outPut)

            print('products: ' + str(len(ReviewDivider.productDic)) + ' / total products: ' + str(productCount))
            print('unprocessed: ' + str(len(ReviewDivider.absentDic)) + ' / total words: ' + str(wordCount))
            print('total reviews: ' + str(len(ReviewDivider.completeReviewList)))
            print(str(number) + '. Show 20 Most frequent products')
            number += 1
            print(str(number) + '. Show 20 Most frequent unprocessed words')
            number += 1
            print(str(number) + '. Search product')
            number += 1
            print(str(number) + '. Manage product dictionary')
            number += 1
        print(str(number) + '. Input new data')
        print('')
        print('b. Back')
        inputValue = input('=> ')

        if noData:
            if inputValue == '1':
                outPut = ReviewDivider.Proceed()
                return ReviewDictionaryMenu(outPut)
        else:
            if inputValue == '1':
                ShowFrequentWord(20, ReviewDivider.dividDic, 0, 1, '', '20 Most frequent products')
                continue
            elif inputValue == '2':
                ShowFrequentWord(20, ReviewDivider.absentDic, 0, 1, '', '20 Most frequent unprocessed words')
                continue
            elif inputValue == '3':
                ShowSearchResult(ReviewDivider.dividDic, 0, ['Count#1'], '', 'Search Product Dictionary')
                continue
            elif inputValue == '4':
                ReviewDivider.ManageProduct('Manage product dictionary')
                continue
            elif inputValue == '5':
                outPut = ReviewDivider.Proceed()
                return ReviewDictionaryMenu(outPut)
            
        if inputValue == 'b':
            return ''
        else:
            outPut = 'Please enter correct number or charactor\n'
            continue

def AnalyzeMenu(outPut=''):
    while True:
        ShowTitle(outPut)
        number = 1
        print(str(number) + '. Analyze Product review')
        number += 1
        print(str(number) + '. Analyze Normal words')
        print('')
        print('b. Back')
        inputValue = input('=> ')

        if inputValue == '1':
            outPut = WordSimilarity.Proceed('Product', 'Similarity Analyzer\n')
            continue
        elif inputValue == '2':
            outPut = WordSimilarity.Proceed('Normal', 'Similarity Analyzer\n')
            continue
        elif inputValue == 'b':
            return ''
        else:
            outPut = 'Please enter correct number or charactor\n'
            continue

def ShowMainMenu():
    print('1. Normal word Dictionary')
    print('2. Review Dictionary')
    print('3. Analyze')
    print('q. Quit')
    inputValue = input('=> ')

    if inputValue == '1':
        return NormalWordDictionaryMenu()
    elif inputValue == '2':
        return ReviewDictionaryMenu()
    elif inputValue == '3':
        return AnalyzeMenu()
    elif inputValue == 'q':
        exit()
    else:
        return 'Please enter correct number or charactor\n'


if __name__ == '__main__':
    baseDir = os.getcwd()
    DictionaryBuilder.baseDir = baseDir
    ReviewDivider.baseDir = baseDir
    WordSimilarity.baseDir = baseDir

    outPut = ''
    while True:
        ShowTitle(outPut)
        outPut = ShowMainMenu()
