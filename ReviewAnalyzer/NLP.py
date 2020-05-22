import MeCab

def DoNLP(rawData, targetTag='None', Mode='Review'):
    words = rawData.split(' ')
    for word in words:
        if word.__contains__('@') == True or word.__contains__('http') == True:
            words.remove(word)

    rawData = ''
    for word in words:
        rawData = rawData + word + ' '

    exceptTag = ['NNB', 'VCP', 'VCN', 'XSN', 'XSV', 'XSA', 'MAG', 'MAJ', 'IC', 'JKS',
                    'JKC', 'JKG', 'JKO', 'JKB', 'JKM', 'JKI', 'JKQ', 'JC', 'JX', 'ETM', 'ETN', 
                    'EP', 'EF', 'EC', 'VX', 'SC', 'SF', 'SE', 'SSO', 'SSC', 'SY', 'SN', 'UNKNOWN']
    connectTag = ['NNG', 'NNP', 'SL', 'SN', 'SY']
    exceptSymbal = ['.', '+']
    resultString = []
    tagedData = MeCab.Tagger().parse(rawData)

    # print(tagedData)

    resultData = tagedData.split('\n')
    dataList = []

    for data in resultData:
        dataSet = []
        splitData = data.split('\t')
        if len(splitData) == 2:
            word = splitData[0]
            tagDetail = splitData[1].split(',')
        else:
            continue
        
        tag = tagDetail[0]
        tagType = tagDetail[4]
        firstTag = tagDetail[5]
        expression = tagDetail[7]

        if tag == 'MAG':
            if tagDetail[1] == '*':
                continue
            MAGtype = tagDetail[1].split('|')[1]
            if MAGtype != '부정부사':
                continue

        if tagType == 'Inflect':
            word = expression.split('/')[0]
            tag = firstTag

        dataSet.append(word)
        dataSet.append(tag)

        dataList.append(dataSet)

    index = 0
    while True:
        if index >= len(dataList):
            break

        data = dataList[index]

        if Mode == 'Review':
            if data[1] == 'EC':
                if index - 1 >= 0 and index + 1 < len(dataList):
                    if dataList[index + 1][1][0] == 'V':
                        if dataList[index + 1][1] == 'VV':
                            index += 1
                            continue
                        if dataList[index - 1][0][len(dataList[index - 1][0]) - 1] == '다':
                            dataList[index - 1][0] = dataList[index - 1][0][:len(dataList[index - 1][0]) - 1]
                        dataList[index - 1][0] = dataList[index - 1][0] + data[0] + ' ' + dataList[index + 1][0]
                        dataList.pop(index + 1)
                        dataList.pop(index)
                        if dataList[index - 1][1][0] == 'V':
                            dataList[index - 1][0] = dataList[index - 1][0] + '다'
                        continue

            if data[1] == 'MM':
                if index + 1 < len(dataList):
                    if dataList[index + 1][1][0] == 'N':
                        data[0] = data[0] + dataList[index + 1][0]
                        data[1] = dataList[index + 1][1]
                        dataList.pop(index + 1)
                        index += 1
                        continue

        if data[1] == 'SN' or data[1] == 'NR':
            if index + 1 < len(dataList):
                targetIndex = index + 1
                if dataList[targetIndex][1] == 'NNBC':
                    data[0] = data[0] + dataList[targetIndex][0]
                    data[1] = 'NR'
                    dataList.pop(targetIndex)

                    if data[1] == 'NR':
                        if index - 1 >= 0:
                            targetIndex = index - 1
                            if dataList[targetIndex][1] == 'NR':
                                dataList[targetIndex][0] = dataList[targetIndex][0] + data[0]
                                dataList.pop(index)
                                continue
                    index += 1
                    continue

        if connectTag.__contains__(data[1]) == True:
            if data[0] == 'vs' or data[0] == 'VS' or data[0] == 'Vs':
                data[1] = 'UNKNOWN'
                if index + 1 < len(dataList):
                    if dataList[index + 1][0] == '.':
                        dataList[index + 1][1] = 'UNKNOWN'
                        index += 2
                continue

            if data[1] == 'SY':
                if len(data[0]) > 1:
                    data[1] = 'UNKNOWN'
                    index += 1
                    continue
                else:
                    if len(set(data[0]) & set(exceptSymbal)) == 0:
                        data[1] = 'UNKNOWN'
                        index += 1
                        continue
                    

            if index - 1 >= 0:
                targetIndex = index - 1
                if data[1] == 'SY':
                    if index - 1 >= 0:
                        if dataList[index - 1][1] == 'SF' or dataList[index - 1][1] == 'SY':
                            dataList.pop(index)
                            continue

                    if index + 1 < len(dataList):
                        if dataList[index + 1][1] == 'SY':
                            index += 1
                            continue
                if connectTag.__contains__(dataList[targetIndex][1]):
                    if data[1] == 'NNG' or dataList[targetIndex] == 'NNG':
                        if rawData.__contains__(dataList[targetIndex][0] + data[0]) == False:
                            index += 1
                            continue
                    if data[1] == 'SY':
                        if rawData.__contains__(dataList[targetIndex][0] + data[0]) == False:
                            data[1] = 'UNKNOWN'
                            index += 1
                            continue
                    if rawData.__contains__(dataList[targetIndex][0] + data[0]) == False:
                        dataList[targetIndex][0] = dataList[targetIndex][0] + ' '
                    dataList[targetIndex][0] = dataList[targetIndex][0] + data[0]
                    dataList[targetIndex][1] = 'NNP'
                    dataList.pop(index)
                    continue

        if data[1][0] == 'V':
            data[0] = data[0] + '다'
            index += 1
            continue

        if data[1] == 'MAG':
            if index + 1 < len(dataList):
                data[0] = data[0] + dataList[index + 1][0]
                data[1] = dataList[index + 1][1]
                if data[1][0] == 'V':
                    data[0] = data[0] + '다'
                dataList.pop(index + 1)
                index += 1
                continue

        if data[1] == 'XPN':
            if index + 1 < len(dataList):
                targetIndex = index + 1
                if dataList[targetIndex][1] == 'NNG':
                    dataList[targetIndex][0] = data[0] + dataList[targetIndex][0]
                    dataList.pop(index)
                    index += 1
                    continue

        index += 1
        
    for data in dataList:
        if targetTag == 'None':
            if exceptTag.__contains__(data[1]) == False:
                resultString.append(data[0])
        else:
            if data[1] == targetTag:
                resultString.append(data[0])

    return resultString