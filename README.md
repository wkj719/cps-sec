# cps-sec
사용자 방문기록 크롤링 및 분석 프로젝트

#팀원
김동길 박정우 윤성민

# 사용 라이브러리 및 버전
    
Konlpy
    
Scikit-Learn
    
TextRank

# 파일 설명
    
    - CPS_Project_NLP.py
    크롬 헤드라인을 수집하여 웹사이트 사용 패턴을 분석하고, 보안 위협 키워드가 발견되면 메시지를 전송
    
    - Server.py
    메시지 전송을 받기 위한 통신 기능 수행
   
    -stopwords.txt
    분석에서 제외한 불용어가 저장된 텍스트 파일
    
    -headline.txt
    분석에 사용할 크롬 헤드라인이 저장될 텍스트 파일
