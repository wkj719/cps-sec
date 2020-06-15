## CPS-SEC Project
웹 사용기록 크롤링 및 키워드 분석을 통한 보안위협 탐지 프로그램
- 팀원
    - 산업보안학과 김동길
    - 산업보안학과 박정우    
    - 산업보안학과 윤성민

### 사용 라이브러리 및 버전
- Python(3.8.2)
- Konlpy(0.5.2)
- JPype1(0.7.5)  
- Scikit-Learn(0.23.1)
- Numpy(1.18.4)
- Pywin32(227)

### 파일 설명
- CPS_Project_NLP.py : 크롬 헤드라인을 수집하여 웹사이트 사용 패턴을 분석하고, 보안 위협 키워드가 발견되면 메시지를 전송
- TextHandling: 텍스트 파일(헤드라인) 읽어서 전처리 후 반환
- KonlpySentences: 문장 분할 및 단어(명사) 추출 기능
    GraphMatrix: 단어 그래프 및 단어장(딕셔너리) 생성
    Ranking: 단어의 순위값 계산
    TextRank: 단어를 순위에 따라 정렬 후 10개까지 반환
    ChromeThread: 크롬 브라우저 헤드라인 수집 및 주기적으로 분석 실행, 경고메시지 전송        
    
- Server.py

: 메시지 전송을 받기 위한 통신 기능 수행
   
- stopwords.txt

: 분석에서 제외할 불용어가 저장된 텍스트 파일
    
- headline.txt

: 분석에 사용할 크롬 헤드라인이 저장될 텍스트 파일

### Work Flow

1. win32gui를 사용하여 크롬 헤드라인을 수집, headline.txt에 저장
        
       4초 주기로 현재 페이지의 헤드라인 수집

2. headline.txt에 저장된 내용을 불러와 konlpy로 분석하여 키워드 추출

       stopwords.txt의 불용어 목록을 분석 대상에서 제외
       kkma, okt를 사용하여 문장 별 분할 후 명사 추출

3. Scikit-learn을 사용하여 단어 벡터화 및 가중치 부여

4. TextRank 알고리즘을 사용하여 키워드 순위화 후 핵심 키워드 출력

        순위 높은 순서대로 최대 10개까지 출력

5. 분석 완료 후 headline.txt 내용 초기화

        3시간 분량의 새로운 핵심 키워드 분석

6. 1-5번 과정을 3시간 주기로 실행

7. 보안 위협 키워드 발견 시 경고 메시지 전송

### 시행착오 과정
- 데이터 수집 과정

    - 기존에 계획했던 방문기록 수집 방법은 사용자의 로컬 DB의 크롬 히스토리 파일에 저장된 방문기록을 사용하는 것이었다. 그러나 SQLite3를 사용하여 데이터를 가져오는 것에는 성공했지만 크롬 브라우저가 실행 중일 때에는 데이터베이스에 접근할 수 없다는 문제가 나타났다.

    - 이러한 문제를 해결하기 위해 크롬 브라우저가 실행 중이지 않을 때에만 크롬 히스토리 파일에 접근하는 코드를 작성하려고 시도했으나, 생각보다 내용이 복잡하고 효율적이지 않다고 판단하여 Python의 다른 함수 및 기능을 찾아보았다. 이 때 getforegroundwindow, getwindowtext 함수와 스레드 기능을 활용하여 실시간으로 사용 중인 프로세스의 헤드라인을 수집할 수 있는 방법을 알아냈다. 크롬 히스토리에 저장된 방문기록과 헤드라인의 내용이 거의 동일했기 때문에 방문기록 대신 헤드라인을 분석 대상으로 대체하였다.

- 미러링 기능

    - 사용자가 임의로 방문기록을 삭제할 수 있다는 문제가 있었기 때문에 방문기록을 미러링하여 저장함으로써 이를 해결하려 시도했다. 그러나 예상과 달리 미러링 기능을 구현하는 난이도가 높았고 프로젝트에 필수적인 기능이 아니라는 판단 하에 이 문제는 조직정책을 통해 해결하기로 결정했다. 다행히 이후 방문기록이 아닌 헤드라인을 수집하는 것으로 프로젝트를 변경하였고, 수집이 실시간으로 이루어지기 때문에 사용자가 임의로 삭제하기 어려워져 이에 대한 우려를 일정부분 해결할 수 있었다.

- 분석 정확도 개선 (수정)

    - 프로젝트 후반에 팀원들이 가장 고민했던 것은 분석 정확도를 높일 수 있는 방법이었다. 이 과정에서 보안 위협 키워드의 비교, 분석 단계에서 단어 유사도 분석 기능을 구현함으로써 유의어 탐지 기능을 추가하는 것이 아이디어로 제시되었다. 구체적으로는 Scikit-learn 라이브러리의 한 기능을 활용하여 문장 내 빈도수와 역 문헌 빈도수를 계산하여 만든 TF-IDF 모델을 토대로 단어에 벡터 값을 주고, 코사인 유사도 분석을 수행하는 방법을 시도해보았다. 그러나 이 방법을 사용하기 위해서는 TF-IDF 그래프를 생성할 때 충분한 양의 데이터를 수집해야 했지만 3시간 주기로 수집한 텍스트로는 부족했고, TF-IDF 모델을 토대로 부여한 단어 벡터 값은 유사도 분석에 적합하지 않아 유의미한 결과를 얻을 수 없었다.

    - 위 방법 대신 머신러닝 워드임베딩을 사용하고자 시도했다. 한국어 워드 임베딩에 적합한 라이브러리인 kor2vec을 활용해 기존에 있던 학습된 모델을 가져와 유사도를 계산하려고 하였으나, 이 방법을 찾았을 때는 최종발표 기한이 거의 남지 않은 시기여서 공부 및 코드작성을 위한 시간이 충분하지 않았다. 그래서 새로운 기능의 추가보다는 프로젝트의 마무리에 집중하기로 결정했고 결국 해당 기능을 추가하지는 못하였다.

### 추후 개선 및 연구방향(수정)
- 정확도 개선

이 프로젝트는 자연어 처리를 활용해 텍스트 키워드 분석을 하는 프로젝트이기 때문에 분석의 정확도가 그 무엇보다 중요하다. 따라서 추후 분석 정확도를 높일 수 있는 방향으로 연구를 진행하는 것이 우선 과제일 것이다. 분석 정확도를 높이기 위해 시행착오 과정에서 미처 완성하지 못했던 워드임베딩을 활용한 키워드 유의어 탐지 기능의 추가와 이를 추가했을 시의 보안 위협 오탐율에 대한 연구가 추가적으로 진행될 수 있을 것이다. 
또한 본 프로젝트를 진행하며 보안 위협 키워드, 키워드 분석 주기 및 헤드라인 텍스트 분량 설정 등 연구의 정확도에 영향을 줄 수 있는 매개변수에 대해서는 프로그램을 사용하는 조직환경 및 산업분류에 영향을 크게 받을 것이라 판단하여 연구를 깊이 진행하지는 않았다. 하지만 추후 조직환경 및 산업분류 별 시나리오를 구성하고 그에 따른 변별력 있는 보안 위협 키워드 연구 및 분석 매개변수 설정 등의 연구를 진행한다면 프로젝트의 분석 정확도 개선 및 완성도를 높일 수 있을 것이다.

- CPS를 활용한 대응방안

위협 키워드가 발견되었을 때 단순히 이를 보안 관리자에게 전송하는 것을 넘어, 보안 관리자가 CPS를 통해 즉각적으로 대응할 수 있는 방안에 대해 생각해보고자 한다. 가령 아두이노를 이용해 콘센트를 제어, 모니터의 전원을 직접적으로 차단하는 방법을 사용할 수 있다. 내부위협에 물리적으로 대응할 수 있다는 점에서 유의미한 연구가 될 것이다.

- 분석 결과의 다른 활용 방안

본 프로젝트에서는 웹 사용기록 텍스트 분석을 통해 추출한 키워드를 보안 위협 키워드와 비교 분석하여 보안 위협 탐지에만 활용했다. 그러나 추출된 키워드를 통해서는 보안 위협 탐지 뿐만 아니라 사용자의 웹 사용 패턴 및 사용자 행위 분석, 업무집중도 등의 다른 지표를 분석하는 데에도 활용할 수 있을 것이다. 이와 관련하여 본 프로젝트를 활용하여 충분한 키워드 분석 결과 및 통계자료 등의 데이터가 쌓인다면, 추후 ‘키워드 분석을 통해 도출한 사용자 업무집중도와 보안사고 발생 확률 간의 상관관계’, ‘웹 사용패턴 분석을 통한 사용자 분류와 보안의식 점수의 상관관계’ 등 키워드 분석 결과를 활용해 다양한 보안 관련 연구를 진행할 수도 있을 것이다.

### 차별화되는 강점
-	팀원들의 노력과 프로젝트 발전 정도
프로젝트 초기 제안 당시에는 팀원들의 부족한 코딩 실력과 비슷한 프로젝트를 진행 해본적이 없는 경험 부재로 실습 때 배운 웹 크롤링과 자연어처리 라이브러리 기능을 단순히 사용만 하는 간단한 프로그램을 제안했다. 하지만 프로젝트를 진행하면서 다양한 피드백과 이를 수용하고 프로젝트를 발전시키기 위한 팀원들의 연구와 노력으로 프로젝트 초기 제안 당시보다 많이 발전된 프로그램을 개발할 수 있었다. 이런 점에 있어서, 다른 조보다 객관적인 코딩 실력이나 프로그램 결과물은 부족할 수 있지만 피드백을 수용하며 연구하고, 토의하며 프로젝트를 개선시키고자 하는 노력과 초기 제안보다 프로젝트가 발전된 정도는 다른 조들보다 앞선 강점이라고 생각한다.

### 프로젝트를 통해 얻은 것

- 파이썬 활용 능력

직접 여러가지 라이브러리를 공부하며 프로젝트를 진행한 결과 파이썬을 활용할 수 있는 능력이 크게 발전하였다. 특히 프로그램의 기능 구현을 위해 적합한 라이브러리를 찾는 과정이 큰 도움이 되었다.

- 자연어처리에 대한 이해

데이터를 다루기 위해 직접 자연어처리 기능을 사용해 봄으로써 자연어처리에 대해 보다 깊이 이해하게 되었다.

- 프로젝트 수행 경험

주제 선정부터 시행착오, 기능 구현 및 개선방안에 대한 고민까지 일련의 프로젝트 과정을 수행함으로써 경험을 쌓아 향후 프로젝트를 진행할 때 더 잘 할 수 있을 것이라는 자신감이 생겼다.
