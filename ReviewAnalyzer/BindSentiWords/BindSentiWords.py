# -*- coding: utf-8 -*-
"""
사용법:
    
    # step1. 클래스 객체를 선언합니다
    bsw = BindSentiWords
    
    # step2. 여기에 감정이 비슷한지 확인할 문자열 리스트를 넣습니다.
    a = [ "좋다", "니가 너무 좋다", "좋아서... 죽을 것 같다...", ...]
    returnValue = bsw.BindSentiWords(bsw, a)
    
    # step3. 확인한다.
    print (returnValue['-2'])


함수 BindSentiWords
input:
    리스트를 통해 유사한 단어사전을 받아온다고 가정합니다.
    (list)["기쁘다", "행복하다", "싫다", "디스거스팅", "너무좋다", "좋다", "좋"]

output:
    최종 6개의 리스트를 가지는 2중리스트 로 반환됩니다.
    앞에서부터 감정 +2, +1, 0, -1, -2, None의 값 들 입니다.
    None에 들어간다는 것은 감정사전에 해당하지 않는다는 말입니다.
    그럴 경우 자주나오면 감정사전에 넣어주면 좋겠네요.
    
    (dict), 내부는 (set) 입니다.
    key 는 '-2' ~ '2' 와 'None'이 있음. 문자열 조심할 것.
    value 는 set 형으로 들어있는 단어목록. set는 인덱스가 먹지 않습니다.
    { ['-2'] : ("그릇되다", "두려워하", "맥없이" ...),
     ['-1'] : (""),
     ..
     ['2'] : (""),
     ['None'] : ("") }
    
    ################## 0608 수정됨 ####################################
    
    (dict) 형태로 반환하며
    {
       'word1' : '-1' ,
       'word2' : 'None' ,
       'word3' :  '2'
    }
    같은식입니다.
    
    
principle:
    sentiWord_(-2, -1, 0, 1, 2, None) 파일이 있습니다.
    같은 sentiWord 라인에 있으면 단어를 묶어서 반환합니다...

tip:
    1. None에 해당하는 단어들은, None 폴더에 작성해줍니다.
    딱히 몇 번 나오는지 검사는 안합니다.
    많으면 정리하면 되겠네요.

"""

class BindSentiWords:
    
    keyList = [ '-2', '-1', '0', '1' ,'2']     
    sentiDict = dict()

    def __init__(self):
        # 클래스 생성자입니다.
        # print("BindSentWords Init")
        
        # Senti Dict 불러오기
        # ex) sentiDict['2'] = { [가능하다,가능] , [가장 좋은,가장 좋], ...}
        for key in self.keyList:
            self.sentiDict[key] = []
            with open("sentiWords/SentiWord_" + key + ".txt", encoding="UTF8", mode='r') as f:
                self.sentiDict[key] = set (f.read().split(','))
    
    def BindSentiWords( self, inWordsList ):
        # 초기화
        resultDict = dict()
        
        # 받아온 리스트 단어가 Senti Dict 에 있는지 탐색
        # 만약 존재한다면 resultDict[key] 에 삽입
        # 존재하지 않는다면 resultDict['None'] 에 삽입 
        for word in inWordsList:
            isFound = False
            for key in self.sentiDict.keys():
                if word in self.sentiDict[key]:
                    resultDict[word] = key
                    isFound = True
                    break
            if isFound == False:
                resultDict[word] = 'None'
        
        # None으로 구분된 친구들은 None에 저장한다.
        with open("sentiWords/SentiWord_None.txt", encoding="UTF8", mode='a') as f:
            for word in resultDict.keys():
                if resultDict[word] == 'None':
                    f.write(word +"\n" );
        
        return resultDict

if __name__ == '__main__':
    import time
    bsw = BindSentiWords()
    a = ['a' , '예쁘다', "개예쁘다", "존멋"]
    print("start " + time.ctime())

    print(type(bsw))
    result = bsw.BindSentiWords(a)
    print (result)

    print("end " + time.ctime())
