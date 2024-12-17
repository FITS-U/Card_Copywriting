import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from konlpy.tag import Mecab
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from matplotlib.colors import LinearSegmentedColormap
logging.getLogger("matplotlib").setLevel(logging.WARNING)
def tokenized_vectorize_cosine(card_ctg_list):
    mecab = Mecab()

    # 정규 표현식 수행
    card_ctg_list['ctg_name_list'] = card_ctg_list['ctg_name_list'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","", regex=True)

    # 불용어 정의
    stopwords = ['언제나','지원']
    
    texts = []
    for idx,text in enumerate(card_ctg_list['ctg_name_list']):
        # 형태소 분석
        tokens = mecab.morphs(text)
        print(f"원본 텍스트 [{idx}]: {text}")
        print(f"형태소 분석 결과: {tokens}")
        # 불용어 제거
        tokens = [word for word in tokens if word not in stopwords]
        print(f"불용어 제거 결과: {tokens}")
        print("-" * 50)  # 구분선 추가
        texts.append(" ".join(tokens))


    tfidf_vectorizer = TfidfVectorizer()
    embeddings = tfidf_vectorizer.fit_transform(texts)
    cosine_sim_matrix = cosine_similarity(embeddings)
    print(cosine_sim_matrix)
    similarity_df = pd.DataFrame(
                        cosine_sim_matrix, 
                        index=card_ctg_list['card_id'], 
                        columns=card_ctg_list['card_id']
                        )

    return similarity_df


