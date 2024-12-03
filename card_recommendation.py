import pandas as pd
from interest_calculator import filter_card_benefits_by_user_interest

# 카드별 점수 계산
def calculate_card_scores(card_ctg_list, combined_interest):
    scores = []
    for _, card_row in card_ctg_list.iterrows():
        card_id = card_row['cardId']
        card_categories = card_row['categoryId']
        total_score = 0 # 카드별 점수를 누적할 변수
        for _, interest_row in combined_interest.iterrows():
            if interest_row['categoryId'] in card_categories:
                score = (
                    interest_row['explicit_interest'] + 
                    interest_row['implicit_interest'] / max(1, interest_row['interest_count'])
                )
                total_score += score
        scores.append({
                    'cardId': card_id,
                    'category_score': total_score
                })

    # 점수 데이터프레임 생성
    return pd.DataFrame(scores)

# 사용자별 최고 점수 + 낮은 연회비 카드 선택
def select_top_card_with_low_fee(card_scores, annual_fee_data,top_n=1):
    # 카드 정보에 연회비 추가 (예: domestic_fee)
    card_scores = pd.merge(card_scores, annual_fee_data[['cardId', 'domestic_fee']], on='cardId', how='left')

    # 'category_score'를 내림차순, 'domestic_fee'를 오름차순으로 정렬
    top_card = card_scores.sort_values(by=['category_score', 'domestic_fee'], ascending=[False, True])

    # 가장 높은 점수 및 낮은 연회비를 가진 카드 선택 (top_n개)
    return top_card.head(top_n)


# 사용자별로 가장 유사한 카드 찾기
def get_most_similar_cards(top_cards, similarity_df, num_similar=2):
    recommendations = []

    for _, row in top_cards.iterrows():
        card_id = row['cardId']

        # 유사도를 계산하고 자기 자신을 제외하고 정렬
        similar_cards = similarity_df.loc[card_id].drop(card_id).sort_values(acsending=False)
        
        # 상위 num_similar개의 카드만 선택
        top_similar_cards = similar_cards.head(num_similar)
        # 추천 결과 저장
        for similar_card_id, similarity in top_similar_cards.items():
            recommendations.append({
                "original_cardId": card_id,
                "recommended_cardId": similar_card_id,
                "similarity_score": similarity
            })

    # 추천 결과를 데이터프레임으로 반환
    return pd.DataFrame(recommendations)

# 추천된 카드에서 사용자 관심사 기반 혜택 필터링
def add_user_interest_to_recommendations(recommendations, combined_interest, card_ctg_list, Category):
    # Category 매핑 생성 (효율성 향상)
    category_map = Category.set_index("categoryId")["categoryName"].to_dict()

    filtered_recommendations = []

    for _, rec in recommendations.iterrows():
        recommended_card_id = rec['recommended_cardId']
        
        # 카드 데이터 필터링
        card_data = card_ctg_list[card_ctg_list['cardId'] == recommended_card_id]

        # 사용자 관심 카테고리에 해당하는 카드만 선택
        filtered_cards = filter_card_benefits_by_user_interest(combined_interest, card_data)

        # 교집합 카테고리를 매핑해 이름 리스트로 변환
        if not filtered_cards.empty:
            filtered_cards["intersectionMapped"] = filtered_cards["intersection"].apply(
                lambda ids: [category_map[int(id)] for id in ids if int(id) in category_map]
            )

            # 추천 결과에 필터링된 카드 추가
            filtered_recommendations.append({
                "recommended_cardId": recommended_card_id,
                "mainCtgNameListStr": filtered_cards.iloc[0]['intersectionMapped']
            })

    return pd.DataFrame(filtered_recommendations)


