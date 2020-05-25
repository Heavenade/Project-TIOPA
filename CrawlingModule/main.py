# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 17:45:38 2020

@author: 문성현
"""
# 자작
import stringEdit
import crawling
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


print("크롤링 모듈을 시작합니다.")


#cs = CSetting
#cs.OpenSetting(cs)

siteOptionPath = "SiteOption/"

while True:
    os.system('cls')
    
    #cs.PrintInfo(cs)
    
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
    #elif command.find("2") == 0:
        #cs.InputSetting(cs)
    elif command.find("1") == 0:
        
        process = ""
        ind = 0
        isProcessing = False
        while True:
            siteOptionList = os.listdir("SiteOption")
            if len(siteOptionList) <= 0:
                print("SiteOption에 Option이 없습니다.")
                break
            else:

                cs = CSetting
                cs.OpenSetting(cs, siteOptionPath + siteOptionList[ind])
                process = crawling.DoCrawling(cs)
                if process == "PROCESS":
                    isProcessing = True
                
                if process == "STOP":
                    break
                
                ind = ind + 1
                if ind >= len(siteOptionList):
                    
                    if isProcessing == False:
                        break
                    ind = 0
                    isProcess = False
                    