# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 17:45:38 2020

@author: 문성
"""

import requests
import stringEdit
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from datetime import datetime
import keyboard
import html5lib
import re

"""
혹시라도 프로그램이 안 돌아간다면??? 콘솔창에서
pip install requests
pip install BeautifulSoup
pip install datetime
pip install keyboard
pip install html5lib
pip install re
를 쳐보십시오. 그래도 안되면 잘 모르겠는데... (install이 안되는 라이브러리는 일단 넘어가시오.)
stringEdit은 내가 만든거니까 아마 안쳐도 괜찮을걸요. 파일만있으면.
"""


"""
#############################################################
설정을 열심히 해보십시오
#############################################################
"""
# 긁어오기관련
urlFront = 'http://underkg.co.kr/opinion/'    # 사이트의 URL. 번호부분을 뺀 앞부분
urlBack = ''    # 혹시라도 번호 뒤에 공통적으로 뭐가 나오면 들어갈 부분
fileSiteNumber_START = 2330000    # 사이트 게시글 몇번부터 시작할건가요
SITE_WAY = -1 # 양수면, 점점 최근 게시글을 굴삭해감. 음수면 점점 옛날 게시글로 굴삭해감 (+1/-1로만 하자)

# 저장관련
fileName = "words"  # 저장 할 파일 이름 "words00000.txt", "words00001.txt" ...
fileIndex = 30000       # 저장 할 파일 이름에 들어가는 번호.
SiteUnit = 1000000     # 게시글을 최대 몇 개를 볼건지 (끝나는 시간과 관련있음)
ReviewUnit = 1000       # 게시글을 몇 개 마다 저장할건지 (중간중간 파일 저장시간/파일크기와 관련있음)

# 사용자편의
STOP_KEY = 'q' # 콘솔에서 STOP_KEY를 꾹 누르면 저장하고 종료합니다.

"""
#############################################################
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
        titleName= soup.find('a', {'href':re.compile('http://underkg.co.kr/'+str(siteIndex))} )
        s = processHtmlCodeToEasy (titleName)
        if s != 'None':
            t.append(s)
        
        # 게시글 내용을 해보자    
        # List라는 이름이긴 한데, 어지간하면 하나만 나올듯.
        # 옛날에 리뷰 여러개 할때는 리스트였어...
        
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
            for plus in plusList:
                s = s.replace(plus, '')
            
            if len(s) != 0:
                t.append(s)
        
        if len(t) == 0:
            return ["!e"]

        # 댓글을 해보자
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

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

siteIndex = fileSiteNumber_START
totalReview = 0
isStop = False

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