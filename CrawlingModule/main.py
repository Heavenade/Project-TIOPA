# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 17:45:38 2020

@author: 문성현
"""
# 자작
import stringEdit
#import CSetting # 이건 왜 안되지?
#from stringEdit import *
from CSetting import *

# 공용 라이브러리
import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from datetime import datetime
import keyboard
import html5lib
import re
import os


"""
혹시라도 프로그램이 안 돌아간다면??? 콘솔창에서
pip install requests
pip install BeautifulSoup

... 등등 저 위에있는 import - 를 pip install - 로 바꿔서 쳐보세요.

그래도 안되면 잘 모르겠는데...

cls가 왜 안되지?
"""

def processHtmlCodeToEasy( _str ):
    result = str(_str)
    result = stringEdit.removeCmpSign(result)
    result = stringEdit.replaceSpecialChara(result)
    result = stringEdit.removeSpecialChara(result) 
    result = stringEdit.removeWrongSpace(result)
    return result

def _getComment(_url, siteIndex):
    try:
        html = requests.get(_url).text
        soup = BeautifulSoup(html, 'html5lib')
        
        t = []
        txtList = []

        # 게시글 타이틀을 해보자
        #titleName= soup.find('a', {'href':re.compile('http://underkg.co.kr/'+str(siteIndex))} )
        titleName= soup.find('h1', {'class':re.compile('headline*')} )

        s = processHtmlCodeToEasy (titleName)
        if s != 'None':
            t.append(s)
        
        # 게시글 내용을 해보자    
        # List라는 이름이긴 한데, 어지간하면 하나만 나올듯.
        # 옛날에 리뷰 여러개 할때는 리스트였어...
        txtList = soup.find_all('div', {'id':re.compile('article_body')} )
        
        # 게시글 내용에서 특정 부분(클래스)를 제거하자
        # 먼저 제거할 부분들을 찾아 두고 게시글 내용에 넣기 전에 제거한다.
        plusList = []
        plusTxt = soup.find_all('div', {'class':re.compile('recent_box_part')} )
        for line in plusTxt:
            plusList.append(processHtmlCodeToEasy ( line ))
        
        # 이부분이 진짜 게시글내용을 가져오는 부분
        txtList = soup.find_all('div', {'class':re.compile('document_.*')} )
        for line in txtList:
            s = processHtmlCodeToEasy ( line )
            #for plus in plusList:
            #    s = s.replace(plus, '')
            
            if len(s) != 0:
                t.append(s)
        
        if len(t) == 0:
            return ["!e"]

        # 댓글을 해보자
        if False:
            txtList = soup.find_all('div', {'class':re.compile('comment_.*')} )
            
            for line in txtList:
                s = processHtmlCodeToEasy ( line )
                if len(s) != 0:
                    t.append(s)
        
        if len(t) == 0:
            return ["!e"]

        return t
        
    except:
        return ["!e"]

def PrintCurTime(head = ""):
    now = datetime.now()
    print(str(head) + " time: "+ str(now))

def DoCrawling( _cs ):
    
    siteIndex = _cs.fileSiteNumber_START
    totalReview = 0
    isStop = False
    
    while abs( _cs.fileSiteNumber_START - siteIndex) < _cs.SiteUnit:
        #PrintCurTime("seraching " + str(siteIndex))
        wordIndex = 0
        wordList = []
        
        reviewCount = 0
        siteIndexBefore = siteIndex
        while abs(siteIndexBefore - siteIndex) < _cs.ReviewUnit:       # 게시글이 ReviewUnit개 일 때 마, 파일을 저장함.
            _url = _cs.urlFront + str(siteIndex) + _cs.urlBack
            _coment = _getComment(_url, siteIndex)
            #print(_coment)
            if _coment.__contains__("!e") == False:
                reviewCount = reviewCount + 1
                #print("진 짜 게시글은 " +str(reviewCount) + " 개 째...")
                wordList.append( [siteIndex, _coment] )       # [번호, [리뷰1, 리뷰2, 리뷰3]] 꼴
            siteIndex = siteIndex + _cs.SITE_WAY
            
            #print(str(fileSiteNumber_START - siteIndex) + "개 째...")
            
            if keyboard.is_pressed(_cs.STOP_KEY):
                isStop = True
                break
    
        totalReview = totalReview + reviewCount
        txtFile = open( str(_cs.fileName) + str(_cs.fileIndex).zfill( 5 )+".txt", 'w', -1, "utf-8")
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
    
    _cs.SaveSetting()
    
    print("========= DONE")
    print("저는 할 일을 잘 수행했습니다.")
    print("게시글 " +str(_cs.fileSiteNumber_START) +"부터 " + str(abs(_cs.fileSiteNumber_START-siteIndex)) + "개나!")
    print("리뷰는 " + str(totalReview) + "개나!")
    
    writeStr = "게시글 " +str(_cs.fileSiteNumber_START) +"부터 " + str(abs(_cs.fileSiteNumber_START-siteIndex)) + "개나!"
    writeStr = writeStr + "리뷰는 " + str(totalReview) + "개나!"
    
    txtFile = open( "lastRecord.txt", 'w', -1, "utf-8")
    txtFile.writelines(writeStr)
        
print("크롤링 모듈을 시작합니다.")
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


cs = CSetting
cs.OpenSetting(cs)

while True:
    os.system('cls')
    
    cs.PrintInfo(cs)
    
    print()
    print("############# 메인 화면 #######################")

    print("숫자로 명령어를 입력해주세요.")
    print("1. 크롤링 시작")
    print("2. 세팅 변경")
    print("3. 프로그램 종료")
    print("......................")
    command = input("입력하세요. : ")
    
    if command.find("3") == 0:
        print("프로그램을 종료합니다.")
        break
    elif command.find("2") == 0:
        cs.InputSetting(cs)
    elif command.find("1") == 0:
        DoCrawling(cs)

'''
while abs( fileSiteNumber_START - siteIndex) < SiteUnit:
    PrintCurTime("seraching " + str(siteIndex))
    wordIndex = 0
    wordList = []
    
    reviewCount = 0
    while reviewCount < ReviewUnit:       # 게시글이 ReviewUnit개 일 때 마, 파일을 저장함.
        _coment = _getComment(urlFront + str(siteIndex) + urlBack, siteIndex)
        #print(_coment)
        if _coment.__contains__("!e") == False:
            reviewCount = reviewCount + 1
            #print("진 짜 게시글은 " +str(reviewCount) + " 개 째...")
            wordList.append( [siteIndex, _coment] )       # [번호, [리뷰1, 리뷰2, 리뷰3]] 꼴
        siteIndex = siteIndex + SITE_WAY
        
        #print(str(fileSiteNumber_START - siteIndex) + "개 째...")
        
        if keyboard.is_pressed(STOP_KEY):
            isStop = True
            break

    totalReview = totalReview + reviewCount
    txtFile = open( str(fileName) + str(fileIndex).zfill( 5 )+".txt", 'w', -1, "utf-8")
    print("지금  " + str(reviewCount) + "개를 완료했으니")
    print("   누적 사이트 " +str(fileSiteNumber_START - siteIndex) + " 개로 전체 리뷰 "+ str(totalReview) + "개가 완료되었어용")
    
    for reviewInfo in wordList:
        line = str(reviewInfo[0])
        for review in reviewInfo[1]:
            line = line + "," + str(review)
        
        txtFile.writelines(line + "\n")
    
    txtFile.close()
    fileIndex = fileIndex + 1
    
    if isStop == True:
        PrintCurTime("========= STOP")
        break

print("========= DONE")
print("저는 할 일을 잘 수행했습니다.")
print("게시글 " +str(fileSiteNumber_START) +"부터 " + str(abs(fileSiteNumber_START-siteIndex)) + "개나!")
print("리뷰는 " + str(totalReview) + "개나!")

writeStr = "게시글 " +str(fileSiteNumber_START) +"부터 " + str(abs(fileSiteNumber_START-siteIndex)) + "개나!"
writeStr = writeStr + "리뷰는 " + str(totalReview) + "개나!"

txtFile = open( "lastRecord.txt", 'w', -1, "utf-8")
txtFile.writelines(writeStr)
'''