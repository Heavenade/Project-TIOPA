# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 11:24:29 2019

@author: kimga
"""

import koreanDisassemble as kd

def removeFrontSpace( _str):
    while True:
        spaceInd = _str.find(' ')
        if spaceInd == 0:
            if len(_str) > 0:
                _str = _str[1:]
            else:
                return ""
        else:
            break
    return _str

def removeCmpSign( _str ):
    while True:
        start = _str.find('<')
        dest = _str.find('>')

        if start < dest:
            _str = _str[:start] + _str[dest+1:]
        elif dest > start:
            _str = _str[dest+1:]
        elif start != -1:
            _str = _str[:start]
        elif dest != -1:
            _str = _str[dest+1:]
        else:
            break
        #print(_str)
        """
        if start == -1 and dest == -1:
            result += _str
            break
        
        result += _str[:start]
        if start > dest:
            break
        else:
            _str = _str[dest+1:]
        """

    return _str

def removeOverlapSpace( _str ):
    # 탭, 연속된 스페이스 등을 제거
    result = _str
    while result.find('\t') != -1:
        result = result.replace ('\t', '')
    
    while result.find('  ') != -1:
        result = result.replace('  ', '')
        
    while result.find('\r') != -1:
        result = result.replace('\r', '')

    return result

def removeComma( _str ):
    result = _str
    result = result.replace (',', ' ')
    return result

def removeEnter( _str ):
    _str = _str.replace('\n', ' ')
    return _str

def removeSpace( _str ):
    result = _str
    while result.find(' ') != -1:
        result = result.replace(' ', '')
    return result

def printStringList ( _stringList ):
    for s in _stringList:
        print(s)

def procStringEdit( _str ):
    t = _str
    t = removeCmpSign(t)
    t = removeOverlapSpace(t)
    t = removeSpace(t)
    tList = removeEnter(t)
    sList = []
    for sentence in tList:
        word = kd.korean_to_be_englished(sentence)
        for letter in word:
            for l in letter:
                if l != ' ':
                    sList.append(l)
    return sList
    
def procDivideString( _str ):
    strList = []
    strLen = len(_str)
    size = 1
    start = 0
    
    while size <= strLen:
        start = 0
        while start + size <= strLen:
            strList.append(_str[start:start+size])
            start = start + 1
        size = size + 1
    
    return strList

def procMakeStringFromList( _list ):
    word = ""
    for i in range(len(_list)):
        word = word + _list[i]
    word = word.lower()
    return word

'''
s = "<dd class=\"\" id=\"small_cmt_931472\">\r\n              보수 진보를 봤을때<br/>\n지금 자한당에서 하는짓은 어디에도 <br/>\n속하지 않는데 남보고 좌빨이네 뭐네..<br/>\n왜 우리나라 세금으로 처먹고 사는지?<br/>\n탄핵당한 전 대리인이 영양제 맞고 누워있지를 않나.. 참..<br/>\n재네는 우리나라사람 맞나 싶다            </dd>"
t = removeCmpSign(s)
t = removeOverlapSpace(t)
t = removeEnter(t)
printStringList(t)
'''
#print(procDivideString(['ㅎ', 'ㅎ', 'ㅅ', 'ㅣ', 'ㅂ', 'ㅏ']))
#for part in t:
#    print(type(part), part)

#print ( procStringEdit("하이 ㅎㅎ") )