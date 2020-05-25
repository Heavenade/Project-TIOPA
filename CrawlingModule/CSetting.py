# -*- coding: utf-8 -*-
"""
Created on Mon May 18 23:13:23 2020

@author: kimgaejin
"""
import os
import sys

class CSetting:
    # 세팅파일 관련
    settingFileName = "setting.txt"
    
    # 현재 파일 속성
    avaliable = "1"
    
    # 긁어오기관련
    urlFront = ''    # 사이트의 URL. 번호부분을 뺀 앞부분
    urlBack = ''    # 혹시라도 번호 뒤에 공통적으로 뭐가 나오면 들어갈 부분
    fileSiteNumber_START = 0  # 사이트 게시글 몇번부터 시작할건가요
    SITE_WAY = 1 # 양수면, 점점 최근 게시글을 굴삭해감. 음수면 점점 옛날 게시글로 굴삭해감 (+1/-1로만 하자)
    
    textDataRange = [] #[ [TAG_ALL, "h1", "class", "headline mg"] ]
    textDataFilterList = []  #[USER_RANGE, "<!--", "-->"]  ]
    
    # 저장관련
    fileName = "words"  # 저장 할 파일 이름 "words00000.txt", "words00001.txt" ...
    fileIndex = 00000       # 저장 할 파일 이름에 들어가는 번호.
    SiteUnit = 100000     # 게시글을 최대 몇 개를 볼건지 (끝나는 시간과 관련있음)
    ReviewUnit = 1000       # 게시글을 몇 개 마다 저장할건지 (중간중간 파일 저장시간/파일크기와 관련있음)
    
    # 사용자편의
    STOP_KEY = 'q' # 콘솔에서 STOP_KEY를 꾹 누르면 저장하고 종료합니다.
    
    def DelEnter( s ):
        s = s.replace('\n', '')
        return s

    def PrintInfo( self ):
        print()
        print("############# 현재 세팅 #######################")

        _url = self.urlFront + str(self.fileSiteNumber_START) + self.urlBack
        if self.SITE_WAY > 0:
            print("게시글 크롤링은 '" + _url + "' 에 대해서 정방향으로 진행합니다.")
        elif self.SITE_WAY < 0:
            print("게시글 크롤링은 '" + _url + "' 에 대해서 역방향으로 진행합니다.")
        _fileName = str(self.fileName) + str(self.fileIndex).zfill( 5 )+".txt"
        print("파일 이름은 '"+ _fileName + "' 부터 파일당 "+ str(self.ReviewUnit)+ "개마다 저장될 것이고")
        print("총 " + str(self.SiteUnit) + " 개 사이트를 크롤링하면 그만둡니다.")
        print("크롤링하는 데이터의 정보는 다음과 같습니다.")
        for s in self.textDataRange:
            print (s)
        print("크롤링하는 도중, 다음과 같은 정보는 필터링합니다.")
        for s in self.textDataFilterList:
            print (s)
        print("멈추고 싶으면 '"+ str(self.STOP_KEY) + "' 키를 누르세요.")

    
    def OpenSetting( self , _filePath = None ):
         if _filePath == None:
             if os.path.isfile("setting.txt") == False:
                 print("기본 세팅이 없습니다. 세팅에서 정비해주세요.")
                 return False
         
         try:
             self.settingFileName = _filePath
             settingFile = open( self.settingFileName, 'r', -1, "utf-8")
             
             self.avaliable = self.DelEnter ( settingFile.readline() )

             self.urlFront = self.DelEnter ( settingFile.readline() )
             self.urlBack = self.DelEnter ( settingFile.readline() )
             self.fileSiteNumber_START = int ( self.DelEnter ( settingFile.readline() ) )
             self.SITE_WAY = int ( self.DelEnter ( settingFile.readline() ) )
            
             sentence = settingFile.readline().split('\t')
             self.textDataRange = []
             for s in sentence:
                 perOption = s.split(',')
                 options = []
                 for i in perOption:
                     i = i.replace("\n","")
                     options.append(i)
                 if len(options) > 0:
                     self.textDataRange.append(options)
                
             sentence = settingFile.readline().split('\t')
             self.textDataFilterList = []
             for s in sentence:
                 perOption = s.split(',')
                 options = []
                 for i in perOption:
                     i = i.replace("\n","")
                     options.append(i)
                 if len(options) > 0:
                     self.textDataFilterList.append(options)
            
             # 저장관련
             self.fileName = self.DelEnter ( settingFile.readline() )
             self.fileIndex = int ( self.DelEnter ( settingFile.readline() ) )
             self.SiteUnit = int (  self.DelEnter ( settingFile.readline() ) )
             self.ReviewUnit = int ( self.DelEnter ( settingFile.readline() ) )
                    
             self.STOP_KEY = self.DelEnter ( settingFile.readline() ) 
    
             settingFile.close()
             print("기본 세팅이 존재합니다. ",filePath," 파일을 불러옵니다.") 
         except:
             print("error:세팅을 불러오던 도중 실수했습니다.")

         return True
     
    def SaveSetting( self ):
         settingFile = open( self.settingFileName, 'w', -1, "utf-8")
         
         settingFile.writelines(self.avaliable + "\n")
         settingFile.writelines(self.urlFront + "\n")
         settingFile.writelines(self.urlBack + "\n")
         settingFile.writelines(str(self.fileSiteNumber_START) + "\n")
         settingFile.writelines(str(self.SITE_WAY) + "\n")

         s = ""
         dataRange = self.textDataRange
         for i in range(len(dataRange)):
             line = dataRange[i]
             for j in range(len(line)):
                 s = s + line[j]
                 if j != len(line)-1:
                     s = s + ","
             if i != len(dataRange) -1:
                s = s + "\t"
        
         settingFile.writelines(s + "\n")

         s = ""
         dataRange = self.textDataFilterList
         for i in range(len(dataRange)):
             line = dataRange[i]
             for j in range(len(line)):
                 s = s + line[j]
                 if j != len(line)-1:
                     s = s + ","
             if i != len(dataRange) -1:
                s = s + "\t"
        
         settingFile.writelines(s + "\n")

         settingFile.writelines(self.fileName + "\n")
         settingFile.writelines(str(self.fileIndex) + "\n")
         settingFile.writelines(str(self.SiteUnit) + "\n")
         settingFile.writelines(str(self.ReviewUnit) + "\n")
         
         settingFile.writelines(str(self.STOP_KEY) + "\n")

         settingFile.close()
    
    def InputSetting( self ):
        self.PrintInfo(self)

        print("대부분의 기능은 SiteOption에서 직접 수정하길 권장합니다.")
        print("왜냐하면 여기 너무 힘을 많이 쏟으면 손해같거든")
        print("그래서 이제 거의 사용하지 않습니다.")
        print("앵간하면 사용하지 마십쇼.")
        print("")
        print("중요: 변경을 원치 않을 경우, 엔터를 눌러 지나가주세요.")
        
        displayComent = "urlFront("+self.urlFront+"):"
        s = input("urlFront: ")
        if s != "":
            self.urlFront = s
        
        displayComent = "fileSiteNumber_START("+str(self.fileSiteNumber_START)+"):"
        s = input(displayComent)
        if s != "":
            self.fileSiteNumber_START = int(s)
         
        displayComent = "urlBack("+self.urlBack+"):"
        s = input(displayComent)
        if s != "":
            self.urlBack = s
            
        displayComent = "SITE_WAY("+str(self.SITE_WAY)+"):"
        s = input(displayComent)
        if s != "":
            if s == "1" or s == "-1":
                self.SITE_WAY = int(s)
            
        displayComent = "fileName("+self.fileName+"):"
        s = input(displayComent)
        if s != "":
            self.fileName = s
            
        displayComent = "fileIndex("+str(self.fileIndex)+"):"
        s = input(displayComent)
        if s != "":
            self.fileIndex = int(s)
            
        displayComent = "SiteUnit("+str(self.SiteUnit)+"):"
        s = input(displayComent)
        if s != "":
            self.SiteUnit = int(s)
        
        displayComent = "ReviewUnit("+str(self.ReviewUnit)+"):"
        s = input(displayComent)
        if s != "":
            self.ReviewUnit = int(s)
            
        displayComent = "STOP_KEY("+self.STOP_KEY+"):"    
        s = input(displayComent)
        if s != "":
            self.STOP_KEY = s
            
        self.SaveSetting(self)

    
    '''
print("여기 바로 실행돼?")
    
cs = CSetting
#cs.SaveSetting(cs)
cs.PrintInfo(cs)
cs.OpenSetting(cs)
cs.PrintInfo(cs)
cs.InputSetting(cs)
cs.PrintInfo(cs)
'''