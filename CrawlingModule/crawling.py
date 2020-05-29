# -*- coding: utf-8 -*-
"""
Created on Mon May 25 02:15:19 2020

@author: kimgaejin
"""
# 자작
import stringEdit
from CSetting import *

# 공용 라이브러리
import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import keyboard
from datetime import datetime
import html5lib
import re
import os


def PrintCurTime(head = ""):
    now = datetime.now()
    print(str(head) + " time: "+ str(now))

def processHtmlCodeToEasy( _str ):
    # return string
    result = str(_str)
    result = stringEdit.removeCmpSign(result)
    result = stringEdit.replaceSpecialChara(result)
    result = stringEdit.removeSpecialChara(result) 
    result = stringEdit.removeWrongSpace(result)
    return result

def _getComment(_url, siteIndex, dataRange, dataFilter):
    try:

        html = requests.get(_url).text
        soup = BeautifulSoup(html, 'html5lib')

        TAG_ALL = '0'
        USER_RANGE = '1'
        # 태그에 따라 긁은 후
        # 태그 내부에 있는 USER_RANGE 를 확인합니다.
        
        textDataList = []

        textDataRange = dataRange# [ [TAG_ALL, "h1", "class", "headline mg"] ,
                         # [TAG_ALL, "div", "id", "article_body.*"] ]
        textDataFilterList = dataFilter#[  [USER_RANGE, "<!--", "-->"]  ]

        # 크롤링 데이터 문단 떼어내기
        for dataRange in textDataRange:
            if dataRange[0] == TAG_ALL:
                if dataRange[2] == "null":
                    datas = soup.find_all(dataRange[1])
                else:
                    datas = soup.find_all(dataRange[1], {dataRange[2]:re.compile(dataRange[3])})
                for data in datas:
                    textDataList.append(str(data))
        
        needPartDatas = []
        # 필요없는 내용 삭제
        for textData in textDataList:
            rawData = textData
            for dataRange in textDataFilterList:
                if dataRange[0] == TAG_ALL:
                    if dataRange[2] == "null":
                        rawData = rawData.replace(soup.find_all(dataRange[1], ''))
                    else:
                        rawData = rawData.replace(soup.find_all(dataRange[1], {dataRange[2]:re.compile(dataRange[3])}), '')

                
                elif dataRange[0] == USER_RANGE:
                    
                    while True:
                        s = rawData.find(dataRange[1])
                        e = rawData.find(dataRange[2])

                        if s == -1 or e == -1:
                            break
                        else:
                            isContinue = False
                            while True:
                                if s > e:
                                    e = rawData[e+1:].find(dataRange[2])
                                    if e == -1:
                                        isContinue = True
                                        break
                                else:
                                    break

                        if isContinue:
                            continue
                        
                        rawData = rawData.replace(rawData[s:e+len(dataRange[2])], '')

            needPartDatas.append(rawData)

        # 편집
        resultData = []
        for textData in needPartDatas :
            s = processHtmlCodeToEasy (textData)
            if len(s) > 0:
                resultData.append(s)
                #print(s)
                
        # 반환
        if len(resultData) > 0:
            return resultData
        else:
            return ["!e"]
          
    except:
        #print("GETCOMMNET_EXCEPT!")
        return ["!e"]

def DoCrawling( _cs ):
    # return "UNUSE", "STOP", "PROCESS", "ERROR"
    
    if _cs.avaliable == "0":
        return "UNUSE"
    
    _cs.PrintInfo(_cs)
    siteIndex = _cs.fileSiteNumber_START
    totalReview = 0
    isStop = False
    isError = False
    
    repeatCount = 0
   # while abs( _cs.fileSiteNumber_START - siteIndex) < _cs.SiteUnit:
    while repeatCount < _cs.SiteUnit:
        PrintCurTime("seraching " + str(siteIndex))
        wordList = []
        
        reviewCount = 0
        siteIndexBefore = siteIndex
        errorDetection = 0
        while abs(siteIndexBefore - siteIndex) < _cs.ReviewUnit:       # 게시글이 ReviewUnit개 일 때 마, 파일을 저장함.
            _url = _cs.urlFront + str(siteIndex) + _cs.urlBack
            _coment = _getComment(_url, siteIndex, _cs.textDataRange, _cs.textDataFilterList)
            #print(_coment)
            if _coment.__contains__("!e") == False:
                reviewCount = reviewCount + 1
                #print("진 짜 게시글은 " +str(reviewCount) + " 개 째...")
                wordList.append( [siteIndex, _coment] )       # [번호, [리뷰1, 리뷰2, 리뷰3]] 꼴
            else:
                errorDetection = errorDetection + 1
            siteIndex = siteIndex + _cs.SITE_WAY
            
            #print(str(fileSiteNumber_START - siteIndex) + "개 째...")
            
            if keyboard.is_pressed(_cs.STOP_KEY):
                isStop = True
                break
            repeatCount = repeatCount + 1
            
        if errorDetection >= _cs.ReviewUnit - 1:
            print("")
            print("###############################################")
            print(errorDetection, _cs.ReviewUnit)
            print("너무 많은 오류를 발견했기에, 이번 단계는 저장하지 않고")
            print("해당 사이트 옵션 또한 unavailiable 로 바꾼 후 옵션을 저장합니다.")
            print("옵션을 다시 확인해주세요.")
            _cs.avaliable = "0"
            _cs.SaveSetting(_cs)
            isError = True
            break
        
        totalReview = totalReview + reviewCount
        txtFile = open( "Datas/"+ str(_cs.fileName) + str(_cs.fileIndex).zfill( 5 )+".txt", 'w', -1, "utf-8")
        print("")
        print("지금  " + str(reviewCount) + "개를 완료했으니")
        print("   누적 사이트 " +str(_cs.fileSiteNumber_START - siteIndex) + " 개로 전체 리뷰 "+ str(totalReview) + "개가 완료되었어용")
        
        for reviewInfo in wordList:
            line = str(reviewInfo[0])
            for review in reviewInfo[1]:
                line = line + "," + str(review)
            
            txtFile.writelines(line + "\n")
        
        txtFile.close()
        _cs.fileIndex = _cs.fileIndex + 1
        
        if isStop == True:
            PrintCurTime("========= STOP")
            break
    
    _cs.fileSiteNumber_START = siteIndex
    _cs.SaveSetting(_cs)
    
    print("========= DONE")
    print("저는 할 일을 잘 수행했습니다.")
    print("게시글 " +str(_cs.fileSiteNumber_START) +"부터 " + str(abs(_cs.fileSiteNumber_START-siteIndex)) + "개나!")
    print("리뷰는 " + str(totalReview) + "개나!")
    
    writeStr = "게시글 " +str(_cs.fileSiteNumber_START) +"부터 " + str(abs(_cs.fileSiteNumber_START-siteIndex)) + "개나!"
    writeStr = writeStr + "리뷰는 " + str(totalReview) + "개나!"
    
    txtFile = open( "lastRecord.txt", 'w', -1, "utf-8")
    txtFile.writelines(writeStr)
    
    if isError == True:
        return "ERROR"
    if isStop == True:
        return "STOP"
    return "PROCESS"
    
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
