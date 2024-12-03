import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

# 카드 혜택 데이터를 벡터화
def vectorize_card_data(card_ctg_list):
    vectorizer = CountVectorizer()
    ctg_matrix = vectorizer.fit_transform(card_ctg_list['mainCtgNameListStr'])

    return ctg_matrix, vectorizer.get_feature_names_out()


def calculate_card_similarity(ctg_matrix, card_ctg_list):
    # 희소 행렬로 계산
    cate_sim = cosine_similarity(csr_matrix(ctg_matrix))
    similarity_df = pd.DataFrame(cate_sim, index=card_ctg_list['cardId'], columns=card_ctg_list['cardId'])
    return similarity_df