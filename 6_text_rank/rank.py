from newspaper import Article
from konlpy.tag import Kkma
from konlpy.tag import Twitter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
import numpy as np

# newspaper 모듈에서 Article 클래스를 import
# Konlpy 모듈에서 Kkma와 Twitter 클래스를 import
# scikit-learn 모듈에서 TfidfVectorizer, CountVectorizer, normalize 클래스를 import
# NumPy를 np로 alias하여 import

class SentenceTokenizer(object):
    def __init__(self):
        # Kkma와 Twitter 객체 생성
        self.kkma = Kkma()
        self.twitter = Twitter()
        # 불용어(stopwords) 리스트 정의
        self.stopwords = ['중인', '만큼', '마찬가지', '꼬집었', "연합뉴스", "데일리", "동아일보", "중앙일보", "조선일보", "기자"
             ,"아", "휴", "아이구", "아이쿠", "아이고", "어", "나", "우리", "저희", "따라", "의해", "을", "를", "에", "의", "가",]

    # URL을 입력받아 문장으로 분리하는 함수
    def url2sentences(self, url):
        # Article 객체 생성
        article = Article(url, language='ko')
        article.download()
        article.parse()
        # Kkma를 사용하여 텍스트를 문장으로 나눔
        sentences = self.kkma.sentences(article.text)

        # 길이가 10 이하인 문장을 이전 문장에 합치는 작업
        for idx in range(0, len(sentences)):
            if len(sentences[idx]) <= 10:
                sentences[idx-1] += (' ' + sentences[idx])
                sentences[idx] = ''

        return sentences

    # 텍스트를 입력받아 문장으로 분리하는 함수
    def text2sentences(self, text):
        # Kkma를 사용하여 텍스트를 문장으로 나눔
        sentences = self.kkma.sentences(text)
        # 길이가 10 이하인 문장을 이전 문장에 합치는 작업
        for idx in range(0, len(sentences)):
            if len(sentences[idx]) <= 10:
                sentences[idx-1] += (' ' + sentences[idx])
                sentences[idx] = ''

        return sentences

    # 문장 리스트를 입력받아 명사를 추출하는 함수
    def get_nouns(self, sentences):
        nouns = []
        for sentence in sentences:
            if sentence != '':
                # Twitter를 사용하여 명사를 추출하고 불용어를 제거
                nouns.append(' '.join([noun for noun in self.twitter.nouns(str(sentence))
                                       if noun not in self.stopwords and len(noun) > 1]))

        return nouns

class GraphMatrix(object):
    def __init__(self):
        # TfidfVectorizer와 CountVectorizer 객체 생성
        self.tfidf = TfidfVectorizer()
        self.cnt_vec = CountVectorizer()
        # 그래프를 저장할 리스트 초기화
        self.graph_sentence = []

    # 문장 리스트를 입력받아 문장 간 유사도 그래프를 생성하는 함수
    def build_sent_graph(self, sentence):
        # TfidfVectorizer를 사용하여 문장 간의 유사도 행렬 생성
        tfidf_mat = self.tfidf.fit_transform(sentence).toarray()
        # 문장 간의 유사도 그래프 생성
        self.graph_sentence = np.dot(tfidf_mat, tfidf_mat.T)
        return  self.graph_sentence

    # 문장 리스트를 입력받아 단어 간 유사도 그래프와 단어-인덱스 매핑을 생성하는 함수
    def build_words_graph(self, sentence):
        # CountVectorizer를 사용하여 단어 간의 유사도 행렬 생성 및 정규화
        cnt_vec_mat = normalize(self.cnt_vec.fit_transform(sentence).toarray().astype(float), axis=0)
        # 단어와 인덱스를 매핑한 사전 생성
        vocab = self.cnt_vec.vocabulary_
        return np.dot(cnt_vec_mat.T, cnt_vec_mat), {vocab[word] : word for word in vocab}

class Rank(object):
    # 그래프와 damping factor를 입력받아 페이지 랭크를 계산하는 함수
    def get_ranks(self, graph, d=0.85): # d = damping factor
        A = graph
        matrix_size = A.shape[0]
        for id in range(matrix_size):
            A[id, id] = 0 # 대각선 부분을 0으로 설정
            link_sum = np.sum(A[:, id]) # A[:, id] = A[:][id]
            if link_sum != 0:
                A[:, id] /= link_sum
            A[:, id] *= -d
            A[id, id] = 1

        B = (1-d) * np.ones((matrix_size, 1))
        # 연립방정식 Ax = b를 해결하여 페이지 랭크 계산
        ranks = np.linalg.solve(A, B)
        return {idx: r[0] for idx, r in enumerate(ranks)}

class TextRank(object):
    def __init__(self, text):
        # SentenceTokenizer 객체 생성
        self.sent_tokenize = SentenceTokenizer()

        # 입력된 텍스트가 URL인지 확인하여 문장 리스트 생성
        if text[:5] in ('http:', 'https'):
            self.sentences = self.sent_tokenize.url2sentences(text)
        else:
            self.sentences = self.sent_tokenize.text2sentences(text)

        # 문장에서 명사 추출
        self.nouns = self.sent_tokenize.get_nouns(self.sentences)

        # GraphMatrix 객체 생성
        self.graph_matrix = GraphMatrix()
        # 문장 간의 유사도 그래프 및 단어 간의 유사도 그래프 및 단어-인덱스 매핑 생성
        self.sent_graph = self.graph_matrix.build_sent_graph(self.nouns)
        self.words_graph, self.idx2word = self.graph_matrix.build_words_graph(self.nouns)

        # Rank 객체 생성
        self.rank = Rank()
        # 문장 간의 페이지 랭크 및 정렬된 인덱스 생성
        self.sent_rank_idx = self.rank.get_ranks(self.sent_graph)
        self.sorted_sent_rank_idx = sorted(self.sent_rank_idx, key=lambda k: self.sent_rank_idx[k], reverse=True)

        # 단어 간의 페이지 랭크 및 정렬된 인덱스 생성
        self.word_rank_idx =  self.rank.get_ranks(self.words_graph)
        self.sorted_word_rank_idx = sorted(self.word_rank_idx, key=lambda k: self.word_rank_idx[k], reverse=True)

    # 요약 생성 함수
    def summarize(self, sent_num=3):
        summary = []
        index = []
        # 상위 sent_num개의 문장 인덱스 추출
        for idx in self.sorted_sent_rank_idx[:sent_num]:
            index.append(idx)

        index.sort()
        # 정렬된 인덱스를 사용하여 요약문 생성
        for idx in index:
            summary.append(self.sentences[idx])

        return summary

    # 키워드 추출 함수
    def keywords(self, word_num=10):
        rank = Rank()
        # 단어 간의 페이지 랭크 계산
        rank_idx = rank.get_ranks(self.words_graph)
        sorted_rank_idx = sorted(rank_idx, key=lambda k: rank_idx[k], reverse=True)

        keywords = []
        index = []
        # 상위 word_num개의 단어 인덱스 추출
        for idx in sorted_rank_idx[:word_num]:
            index.append(idx)

        # 정렬된 인덱스를 사용하여 키워드 생성
        for idx in index:
            keywords.append(self.idx2word[idx])

        return keywords

# 테스트할 URL 주소
url = 'http://v.media.daum.net/v/20170611192209012?rcmd=r'
# TextRank 객체 생성
textrank = TextRank(url)
# 요약문 출력
for row in textrank.summarize(3):
    print(row)
    print()
# 키워드 출력
print('keywords :', textrank.keywords())
