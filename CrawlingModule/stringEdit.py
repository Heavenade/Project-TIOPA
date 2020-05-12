# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 11:24:29 2019

@author: kimga
"""

def removeCmpSign( _str ):
    # < > 사이에 있는 요소들을 제거합니다.
    # 예를들면 <br>
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

    return _str

def removeWrongSpace( _str ):
    # 연속된 띄어쓰기가 나오지 않을 때 까지 제거합니다.
    # 가장 첫 번째 문자가 스페이스바 인 때도 제거합니다.
    result = _str
    while result.find('  ') != -1:
        result = result.replace('  ', '')

    if len(result) > 1:
        if result[0] == ' ':
            result = result[1:]
    elif len(result) == 1:
        if result[0] == ' ':
            result = ""

    return result

def removeSpecialChara( _str ):
    # 특수문자를 "제거" 해야할 때 사용합니다
    # 현재 사용하는 것은 '\t'와 '\n'
    result = _str
    result = result.replace ('\t', ' ')
    result = result.replace ('\n', ' ')
    
    return result

def replaceSpecialChara( _str ):
    # 특수문자를 "변경" 해야할 때 사용합니다
    # 현재 사용하는 것은 ',' => ';'
    result = _str.replace(',', ';')
    return result
