import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# 카드 혜택 데이터를 벡터화
def vectorize_card_data(card_ctg_list):
    vectorizer = CountVectorizer()
    ctg_matrix = vectorizer.fit_transform(card_ctg_list['mainCtgNameListStr'])
    print("ctg_matrix 데이터:\n", ctg_matrix.toarray())

    return ctg_matrix, vectorizer.get_feature_names_out()

    
# 코사인 유사도 계산
# def calculate_card_similarity(ctg_matrix, card_ctg_list):
#     cate_sim = cosine_similarity(ctg_matrix, ctg_matrix)
#     similarity_df = pd.DataFrame(cate_sim, index=card_ctg_list['cardId'], columns=card_ctg_list['cardId'])
#     return similarity_df
def calculate_card_similarity(ctg_matrix, card_ctg_list):
    # 밀집 배열로 변환
    ctg_matrix_dense = ctg_matrix.toarray()
    print("ctg_matrix_dense shape:", ctg_matrix_dense.shape)
    print("ctg_matrix_dense 데이터:\n", ctg_matrix_dense[:5, :5])
    # 코사인 유사도 계산
    cate_sim = cosine_similarity(ctg_matrix_dense, ctg_matrix_dense)
    print("코사인 유사도 행렬 크기:", cate_sim.shape)

    # DataFrame 생성
    similarity_df = pd.DataFrame(cate_sim, index=card_ctg_list['cardId'], columns=card_ctg_list['cardId'])
    return similarity_df