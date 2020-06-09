import os
import DictionaryBuilder
import ReviewDivider
import WordSimilarity
import DataBaseManager

result = None

def ShowTitle(outPut='', currentPosition=''):
    os.system('cls')
    print('Typical Impression Analyzer for Product')
    print(currentPosition, end='')
    print('')
    print(outPut, end='')
    print('')

def ShowFrequentWord(limit, targetDict, outPut=None, title=None):
    if outPut == None:
        outPut = ''
    if title == None:
        title = ''

    SortedDict = {k: v for k, v in sorted(targetDict.items(), key=lambda item: item[1], reverse=True)}

    while True:
        ShowTitle(outPut, title)

        index = 0
        for key, value in SortedDict.items():
            if index >= limit:
                break
            print(str(index + 1) + '. ' + str(key) + ', ' + str(value))
            index += 1

        print('')
        print('b. Return to Main menu')
        inputValue = input('=> ')

        if inputValue == 'b':
            return ''

        outPut = 'Please enter correct number or charactor\n'

def ShowSearchResult(targetDict=None, targetKey=None, isProduct=None, outPut=None, title=None):
    if outPut == None:
        outPut = ''
    if title == None:
        title = ''
    if isProduct == None:
        isProduct = False
        
    while True:
        ShowTitle(outPut, title)

        inputValue = input("Enter word (%q to return): ")
        if inputValue == '':
            outPut = 'Please enter word'
            continue
        if inputValue == '%q':
            return ''
        targetData = inputValue

        resultDict = {}
        if isProduct:
            ReviewDivider.GetProductDic()
            searchResult = ReviewDivider.GetProductName(targetData, targetData)['product_Name']

            if len(searchResult) <= 0:
                outPut = 'No result of ' + targetData
                continue

            for result in searchResult:
                try:
                    detailData = ReviewDivider.productDic[result][targetKey]
                except:
                    detailData = ReviewDivider.productDic[result]
                
                newResult = {result: detailData}
                resultDict.update(newResult)
        else:
            try:
                resultData = targetDict[targetData]
            except:
                outPut = 'No result of ' + targetData
                continue
            else:
                if targetKey != None:
                    detailData = resultData[targetKey]
                else:
                    detailData = resultData

                newResult = {targetData: detailData}
                resultDict.update(newResult)

        outPut = targetData + "\t"
        for key, value in resultDict.items():
            outPut += key + ": " + str(value) + '\n'

def NormalWordDictionaryMenu(outPut=''):
    sqlResult = DataBaseManager.DoSQL("""
    SELECT  Normal_Word, Word_Count
    FROM    similar_word_relation
    WHERE   Normal_Word = Target_Word
    """)
    wordDict = dict(sqlResult)

    sqlResult = DataBaseManager.DoSQL("""
    SELECT  SUM(Word_Count)
    FROM    similar_word_relation
    WHERE   Normal_Word = Target_Word
    """)
    totalWordCount = sqlResult[0][0]

    sqlResult = DataBaseManager.DoSQL("""
    SELECT  COUNT(*)
    FROM    article_dic
    """)
    articleCount = sqlResult[0][0]
    
    while True:
        number = 1
        if len(wordDict) <= 0: 
            ShowTitle('No exist Normal word Dictionary\n' + outPut, 'Normal word Dictionary Menu\n')
        else:
            ShowTitle(outPut)
            print('words: ' + str(len(wordDict)) + ' / total words: ' + str(totalWordCount) + ' / articles: ' + str(articleCount))
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

        if len(wordDict) <= 0:
            if inputValue == '1':
                outPut = DictionaryBuilder.Proceed()
                return NormalWordDictionaryMenu(outPut)
        else:
            if inputValue == '1':
                ShowFrequentWord(20, wordDict, title='20 Most frequent words')
                continue
            elif inputValue == '2':
                ShowSearchResult(wordDict, title='Search Normal word Dictionary')
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
    sqlResult = DataBaseManager.DoSQL("""
    SELECT  Product_Name, Count
    FROM    product_dic
    """)
    productDict = dict(sqlResult)

    sqlResult = DataBaseManager.DoSQL("""
    SELECT  COUNT(*)
    FROM    product_dic
    WHERE   Count > 0
    """)
    existProductCount = sqlResult[0][0]

    sqlResult = DataBaseManager.DoSQL("""
    SELECT  SUM(Count)
    FROM    product_dic
    WHERE   Count > 0
    """)
    totalProductCount = sqlResult[0][0]

    sqlResult =  DataBaseManager.DoSQL("""
    SELECT  COUNT(*)
    FROM    review_dic
    """)
    reviewCount = sqlResult[0][0]
    
    while True:
        number = 1
        if len(productDict) <= 0:
            ShowTitle('No exist Review Dictionary\n' + outPut, 'Review Dictionary Menu\n')
        else:
            ShowTitle(outPut)

            print('products: ' + str(existProductCount) + ' / total products: ' + str(totalProductCount))
            print('total reviews: ' + str(reviewCount) + ' / total product infomation: ' + str(len(productDict)))
            print(str(number) + '. Show 20 Most frequent products')
            number += 1
            print(str(number) + '. Search product')
            number += 1
            print(str(number) + '. Manage product dictionary')
            number += 1
        print(str(number) + '. Input new data')
        print('')
        print('b. Back')
        inputValue = input('=> ')

        if len(productDict) <= 0:
            if inputValue == '1':
                outPut = ReviewDivider.Proceed()
                return ReviewDictionaryMenu(outPut)
        else:
            if inputValue == '1':
                ShowFrequentWord(20, productDict, title='20 Most frequent products')
                continue
            elif inputValue == '2':
                ShowSearchResult(productDict, targetKey='Count', isProduct=True, title='Search Product Dictionary')
                continue
            elif inputValue == '3':
                ReviewDivider.ManageProduct('Manage product dictionary')
                continue
            elif inputValue == '4':
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
