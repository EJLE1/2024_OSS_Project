import requests
from bs4 import BeautifulSoup
import nltk
from collections import Counter
import re

# nltk 불용어 다운로드 (최초 1회 실행 필요)
#nltk.download('stopwords')
from nltk.corpus import stopwords

korean_stopwords = [
    '그', '그리고', '하지만', '더', '이', '저', '그녀', '이것', '저것', '그것', 
    '있다', '없다', '하다', '되다', '이다', '에', '의', '를', '은', '는', '이', '가', '으로', '에서'
]


# 네이버 뉴스에서 <strong class="sa_text_strong"> 텍스트를 크롤링하는 함수
def get_strong_text(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # <strong> 태그 중 class="sa_text_strong"인 항목들 추출
    texts = [strong.get_text() for strong in soup.find_all('strong', class_='sa_text_strong')]
    return texts

# 텍스트 전처리 함수 (불용어 제거, 소문자화, 특수문자 제거 등)
def preprocess_text(text):
    # 불용어 설정 (여기서는 영어와 한국어 불용어 추가)
    stop_words = set(stopwords.words('english')).union(set(korean_stopwords))
    
    # 소문자 변환 및 특수문자 제거
    text = text.lower()  # 소문자 변환
    text = re.sub(r'\W+', ' ', text)  # 특수문자 제거 (공백으로 대체)
    
    # 불용어 제거
    words = [word for word in text.split() if word not in stop_words]
    return words

# 뉴스 제목에서 키워드 빈도 분석 함수
def extract_keywords(texts):
    all_words = []
    for text in texts:
        all_words.extend(preprocess_text(text))  # 각 텍스트를 전처리 후 단어 리스트로 변환
    
    # 키워드 빈도 계산
    word_counts = Counter(all_words)
    
     # 2회 이상 나타난 키워드 필터링 후 빈도순 정렬
    filtered_sorted_keywords = sorted(
        {word: count for word, count in word_counts.items() if count >= 2}.items(),
        key=lambda x: x[1],  # 빈도 기준으로 정렬
        reverse=True          # 내림차순 정렬
    )
    
    return filtered_sorted_keywords

# 네이버 뉴스 경제 섹션 URL
url = 'https://news.naver.com/section/101'
texts = get_strong_text(url)

# 키워드 추출 및 빈도 분석
keywords = extract_keywords(texts)

# 부적합한 단어를 필터링하는 함수
def is_valid_keyword(word):
    # 기준: 2글자 이상, 숫자 및 특수문자가 아닌 단어
    return len(word) > 1 and word.isalpha()

# 키워드만 리스트로 추출하면서 부적합한 단어 제거
keyword_list = [keyword for keyword, freq in keywords if is_valid_keyword(keyword)]

# 키워드 리스트 출력
print("리스트:", keyword_list)
