import os
import DictionaryBuilder
import ReviewDivider

result = None

def ShowTitle(outPut='', currentPosition=''):
    os.system('cls')
    print('Typical Impression Analyzer for Product')
    print(currentPosition, end='')
    print('')
    print(outPut, end='')
    print('')

def NormalWordDictionaryMenu(outPut=''):
    result = DictionaryBuilder.GetExistDicInfo()
    Number = 1
    if result == None:
        ShowTitle('No exist Normal word Dictionary\n' + outPut, 'Normal word Dictionary Menu\n')
    else:
        ShowTitle(outPut)
        print('words: ' + str(result[0]) + ' / total words: ' + str(result[1]) + ' / reviews: ' + str(result[2]))
        print(str(Number) + '. Show 20 Most frequent words')
        Number += 1
        print(str(Number) + '. Edit Representitive word')
        Number += 1
    print(str(Number) + '. Input new data')
    print('b. Return to Main menu')
    inputValue = input('=> ')

    if result == None:
        if inputValue == '1':
            return 'This feature is not ready\n'
    else:
        if inputValue == '1':
            return 'This feature is not ready\n'
        elif inputValue == '2':
            return 'This feature is not ready\n'
        elif inputValue == '3':
            return 'This feature is not ready\n'
        
    if inputValue == 'b':
        return ''
    else:
        return NormalWordDictionaryMenu('Please enter correct number or charactor\n')

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

def ReviewDictionaryMenu(outPut=''):
    result = ReviewDivider.GetExistDicInfo()
    if result != None:
        productDic = result[0]
        absentDic = result[1]
        dividDic = result[2]
        completeDic = result[3]

        productCount = 0
        wordCount = 0
        for dic in dividDic:
            productCount += dic[1]
        for dic in absentDic:
            wordCount += dic[1]
    
    while True:
        Number = 1
        if result == None:
            ShowTitle('No exist Review Dictionary\n' + outPut, 'Review Dictionary Menu\n')
        else:
            ShowTitle(outPut)

            print('products: ' + str(len(productDic)) + ' / total products: ' + str(productCount))
            print('unprocessed: ' + str(len(absentDic)) + ' / total words: ' + str(wordCount))
            print('total reviews: ' + str(len(completeDic)))
            print(str(Number) + '. Show 20 Most frequent products')
            Number += 1
            print(str(Number) + '. Show 20 Most frequent unprocessed words')
            Number += 1
            print(str(Number) + '. Add new product')
            Number += 1
        print(str(Number) + '. Input new data')
        print('b. Return to Main menu')
        inputValue = input('=> ')

        if result == None:
            if inputValue == '1':
                ReviewDivider.Proceed()
                continue
        else:
            if inputValue == '1':
                ShowFrequentWord(20, dividDic, 0, 1, '', '20 Most frequent products')
                continue
            elif inputValue == '2':
                ShowFrequentWord(20, absentDic, 0, 1, '', '20 Most frequent unprocessed words')
                continue
            elif inputValue == '3':
                outPut = 'This feature is not ready\n'
                continue
            elif inputValue == '4':
                outPut = ReviewDivider.Proceed()
                continue
            
        if inputValue == 'b':
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
        return 'This feature is not ready\n'
    elif inputValue == 'q':
        exit()
    else:
        return 'Please enter correct number or charactor\n'


if __name__ == '__main__':
    baseDir = os.getcwd()
    DictionaryBuilder.baseDir = baseDir
    ReviewDivider.baseDir = baseDir

    outPut = ''
    while True:
        ShowTitle(outPut)
        outPut = ShowMainMenu()
