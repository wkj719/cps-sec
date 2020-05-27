from konlpy.tag import Kkma
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
import numpy as np
import csv, sqlite3, os
from datetime import datetime, timedelta

class SQLiteText(object):   # 크롬 히스토리의 방문기록을 텍스트 파일로 저장
    def chrome_history(self):
        connection = sqlite3.connect(os.getenv("APPDATA") + r"\..\Local\Google\Chrome\User Data\Default\history")
        cur = connection.cursor()
        cur.execute("select title from urls")
        results = cur.fetchall()
        f = open("sample.txt", "w", encoding = "UTF-8")
        for r in results:
            print(r)
            f.write(str(r))
            f.write("\n")
        f.close
        
class KonlpySentences(object):  # 문장 분할 및 단어(명사) 추출
    def __init__(self):
        self.kkma = Kkma() # kkma, Okt: Konlpy의 자연어 처리기
        self.okt = Okt()
        # stopwords: 분석에서 제외할 불용어 설정
        self.stopwords = ["네이버", "통합", "검색", "다음", "을", "를", "에", "의", "가", "카페"]

    def divide_sentences(self, text):   # 전체 텍스트를 문장 별로 분할
        sentences = self.kkma.sentences(text)
        for idx in range(0, len(sentences)):
            if len(sentences[idx]) <= 10:
                sentences[idx-1] += (' ' + sentences[idx])
                sentences[idx] = ''
        return sentences

    def get_nouns(self, sentences): # 문장에서 단어(명사)만 추출
        nouns = []
        for sentence in sentences:
            if sentence is not '':
                nouns.append(' '.join([noun for noun in self.okt.nouns(str(sentence))
                if noun not in self.stopwords and len(noun) > 1]))
        return nouns

class GraphMatrix(object):  # 단어 그래프와 {idx: word} 딕셔너리 생성
    def __init__(self):
        self.cnt_vec = CountVectorizer()    # CountVectorizer: 문서 단어 행렬 만드는 메소드
    def get_words_graph(self, sentence):
        cnt_vec_mat = normalize(self.cnt_vec.fit_transform(sentence).toarray().astype(float), axis=0)   # 문서 단어 행렬을 생성해서 배열 반환한 뒤 정규화
        vocab = self.cnt_vec.vocabulary_    # 단어장 {번호: 단어} 생성
        return np.dot(cnt_vec_mat.T, cnt_vec_mat), {vocab[word] : word for word in vocab}   # (단어 그래프, 딕셔너리) 반환

class Ranking(object):  # TF-IDF 그래프에서 {idx: rank} 딕셔너리 생성
    def get_ranks(self, graph, d=0.85): # damping factor는 PageRank의 0.85를 그대로 사용
        A = graph
        matrix_size = A.shape[0]    # 그래프 크기 저장
        for id in range(matrix_size):   # 랭크 값 구하는 식 전개과정
            A[id, id] = 0
            link_sum = np.sum(A[:,id])
            if link_sum != 0:
                A[:, id] /= link_sum
            A[:, id] *= -d
            A[id, id] = 1
        B = (1-d) * np.ones((matrix_size, 1))
        ranks = np.linalg.solve(A, B)
        return {idx: r[0] for idx, r in enumerate(ranks)}

class TextRank(object):
    def __init__(self, text):
        self.ko_sent = KonlpySentences()
        self.sentences = self.ko_sent.divide_sentences(text)
        self.nouns = self.ko_sent.get_nouns(self.sentences)
        self.graph_matrix = GraphMatrix()
        self.words_graph, self.idx2word = self.graph_matrix.get_words_graph(self.nouns)
        self.rank = Ranking()
        self.word_rank_idx =  self.rank.get_ranks(self.words_graph)
        self.sorted_word_rank_idx = sorted(self.word_rank_idx, key=lambda k: self.word_rank_idx[k], reverse=True)

    def get_keywords(self, word_num=20):    # 키워드를 순위에 따라 정렬하여 20개까지 반환
        rank = Ranking()
        rank_idx = rank.get_ranks(self.words_graph)
        sorted_rank_idx = sorted(rank_idx, key=lambda k: rank_idx[k], reverse=True) # 내림차순 정렬
        
        keywords = []
        index=[]
        for idx in sorted_rank_idx[:word_num]:
            index.append(idx)
            
        for idx in index:
            keywords.append(self.idx2word[idx])
        
        return keywords

class TextHandling(object): # 텍스트 파일을 읽어서 전처리한 후 반환
    def text_handle(self, file_path):
        with open(file_path,"r", encoding = 'UTF-8') as t:
            txt = t.read()
            txt = txt.replace("\n",".")
        return txt

s = SQLiteText()
s.chrome_history()
path = r"C:\Users\danawa\AppData\Local\Programs\Python\Python38\CPS\sample.txt" # SQLiteText에서 저장한 텍스트의 경로
h = TextHandling()
txt = h.text_handle(path)
tr = TextRank(txt)
kw = tr.get_keywords()
print(kw)