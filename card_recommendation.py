import pandas as pd
from interest_calculator import filter_card_benefits_by_user_interest

# 카드별 점수 계산
def calculate_card_scores(card_ctg_list, combined_interest):
    scores = []
    for _, card_row in card_ctg_list.iterrows():
        card_id = card_row['cardid']
        card_categories = card_row['categoryid']
        total_score = 0 # 카드별 점수를 누적할 변수
        for _, interest_row in combined_interest.iterrows():
            if interest_row['categoryid'] in card_categories:
                score = (
                    interest_row['explicit_interest'] + 
                    interest_row['implicit_interest'] / max(1, interest_row['interest_count'])
                )
                total_score += score
        scores.append({
                    'cardid': card_id,
                    'category_score': total_score
                })

    # 점수 데이터프레임 생성
    return pd.DataFrame(scores)

# 사용자별 최고 점수 + 낮은 연회비 카드 선택
def select_top_card_with_low_fee(card_scores, annual_fee_data,top_n=1):
    # 카드 정보에 연회비 추가 (예: domestic_fee)
    card_scores = pd.merge(card_scores, annual_fee_data[['cardid', 'domestic_fee']], on='cardid', how='left')

    # 'category_score'를 내림차순, 'domestic_fee'를 오름차순으로 정렬
    top_card = card_scores.sort_values(by=['category_score', 'domestic_fee'], ascending=[False, True])

    # 가장 높은 점수 및 낮은 연회비를 가진 카드 선택 (top_n개)
    return top_card.head(top_n)


# 사용자별로 가장 유사한 카드 찾기
def get_most_similar_cards(top_cards, similarity_df, num_similar):
    recommendations = []

    for _, row in top_cards.iterrows():
        card_id = row['cardid']
        # 유사도를 계산하고 자기 자신을 제외하고 정렬
        similar_cards = similarity_df.loc[card_id].drop(card_id).sort_values(ascending=False)
        
        # 상위 num_similar개의 카드만 선택
        top_similar_cards = similar_cards.head(num_similar)
        # 추천 결과 저장
        for similar_card_id, similarity in top_similar_cards.items():
            recommendations.append({
                "original_card_id": card_id,
                "recommended_card_id": similar_card_id,
                "similarity_score": similarity
            })

    # 추천 결과를 데이터프레임으로 반환
    return pd.DataFrame(recommendations)

# 추천된 카드에서 사용자 관심사 기반 혜택 필터링
def add_user_interest_to_recommendations(recommendations, combined_interest, card_ctg_list, Category):
    # Category 매핑 생성 (효율성 향상)
    category_map = Category.set_index("categoryid")["categoryname"].to_dict()
    final_recommendations = []
    for _, rec in recommendations.iterrows():
        original_card_id = rec['original_card_id']
        recommended_card_id = rec['recommended_card_id']
        
        # 카드 데이터 필터링
        card_data = card_ctg_list[card_ctg_list['cardid'] == recommended_card_id]
        # 사용자 관심 카테고리에 해당하는 카드만 선택
        filtered_cards = filter_card_benefits_by_user_interest(combined_interest, card_data)
        filtered_cards['categoryid'] = filtered_cards['categoryid'].apply(
            lambda x: [str(i).strip() for i in x if str(i).strip().isdigit()] # 공백 제거 후 유효한 ID만 추출
        )
        user_interest_categories = set(combined_interest['categoryid'].astype(str))  # 관심 카테고리 ID를 집합으로 변환

        # filtered_cards['intersection'] = filtered_cards['categoryid'].apply(
        #     lambda categories: list(set(categories) & user_interest_categories)
        # )
        filtered_cards['intersection'] = filtered_cards['categoryid'].apply(
    lambda categories: list(set(categories) & user_interest_categories) if isinstance(categories, list) else []
)

        # intersectionMapped 컬럼 생성
        if not filtered_cards.empty:
            filtered_cards["intersectionMapped"] = filtered_cards["intersection"].apply(
                    lambda ids: [category_map[int(id)] for id in ids if int(id) in category_map]
                )

            # original_card_id 추가
            final_recommendations.append({
                "final_card":original_card_id,
                "mainCtgNameListStr":filtered_cards.iloc[0]['intersectionMapped'],
                "type":"original" # 구분 필드
            })

            # recommended_card_id 추가
            final_recommendations.append({
                "final_card":recommended_card_id,
                "mainCtgNameListStr":filtered_cards.iloc[0]['intersectionMapped'],
                "type":"recommended" # 구분 필드
            })


    return pd.DataFrame(final_recommendations)


