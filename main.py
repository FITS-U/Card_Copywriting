import pandas as pd
from data_handler import preprocess_card_data,preprocess_annual_fee
from interest_calculator import (
    calculate_explicit_interest,
    calculate_implicit_interest,
    merge_interests,
)
from contents import vectorize_card_data, calculate_card_similarity
from card_recommendation import (
    calculate_card_scores,
    select_top_card_with_low_fee,
    get_most_similar_cards,
    add_user_interest_to_recommendations
)
from ad_generator import generate_ads_for_user, process_ad_results
import logging
from flask import Flask, jsonify, request
import pickle
import os

# 로깅 설정
logging.basicConfig(
    filename="debug.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# 테스트용 데이터
test_data = {
    "categories": [
        {"categoryId": 11},
        {"categoryId": 19},
        {"categoryId": 10},
        {"categoryId": 23},
        {"categoryId": 22}
    ],
    "logs": [
        {"categoryId": 8, "eventType": "Click", "clickTime": "2024-12-01T15:26:32.843038"},
        {"categoryId": 9, "eventType": "Click", "clickTime": "2024-12-01T15:26:33.561888"},
        {"categoryId": 18, "eventType": "Click", "clickTime": "2024-12-01T15:26:34.259727"},
        {"categoryId": 26, "eventType": "Click", "clickTime": "2024-12-01T15:26:34.259727"},
        {"categoryId": 29, "eventType": "Click", "clickTime": "2024-12-01T15:26:34.259727"}
    ]
}

# 주어진 데이터
data = [
    {
        "cardId": 43,
        "categoryName": "간편결제",
        "categoryID": 3,
        "benefitTitle": "삼성 페이로 결제 시 10% 할인",
        "description": "온라인 결제 또는 오프라인 결제 중 택1하여 삼성페이로 결제 시 10% 결제일할인( 청구할인), 한도조건: 월 5,000원 (전월 일시불 및 할부 이용금액 30만원 이상 시 제공)"
    },
    {
        "cardId": 43,
        "categoryName": "통신",
        "categoryID": 21,
        "benefitTitle": "이동통신요금 자동납부 시 10% 할인",
        "description": "SKT KT•LG Ut 이동통신요금 자동납부 시 10% 결제일할인(청구할인), 한도조건: 월 5,000원 (전월 일시불 및 할부 이용금액 30만원 이상 시 제공)"
    }
]

# DataFrame으로 변환
Benefit = pd.DataFrame(data)
def preprocess_and_save_data():
    card_info = pd.read_csv("data/CardInfo.csv")
    card_info = card_info[['cardId','cardName','annualFee']]
    card_info = preprocess_annual_fee(card_info)

    card_category = pd.read_csv("data/CardCategory.csv")
    categories_df = pd.read_csv("data/Category.csv")
    card_ctg_list = preprocess_card_data(card_category, categories_df)

    # 벡터화 및 유사도 계산
    ctg_matrix, _ = vectorize_card_data(card_ctg_list)
    similarity_df = calculate_card_similarity(ctg_matrix, card_ctg_list)

    # 데이터 저장
    with open("processed_data.pkl", "wb") as f:
        pickle.dump((card_info, card_ctg_list,similarity_df,categories_df),f)

# 데이터 로드 (API 호출시마다)
def load_preprocessed_data():
    with open("processed_data.pkl","rb") as f:
        card_info, card_ctg_list, similarity_df,categories_df = pickle.load(f)
    return card_info, card_ctg_list, similarity_df,categories_df

app = Flask(__name__)  # Flask 앱 객체 생성

# API에서 호출
@app.route('/generate_ads', methods=['POST'])
def generate_ads():
    try:
        # 미리 준비된 데이터를 불러옴
        card_info, card_ctg_list, similarity_df,categories_df = load_preprocessed_data()

        # JSON 데이터를 DataFrame으로 변환
        categories = test_data.get("categories", [])
        logs = test_data.get("logs", [])
        category_df = pd.DataFrame(categories)
        logs_df = pd.DataFrame(logs)

        # 관심도 계산
        explicit_interest = calculate_explicit_interest(category_df)
        implicit_interest = calculate_implicit_interest(logs_df)
        combined_interest = merge_interests(explicit_interest, implicit_interest)

        # 카드 점수 계산
        card_scores = calculate_card_scores(card_ctg_list, combined_interest)
        if card_scores.empty:
            raise ValueError("Error: card_scores is empty. Check the input data and preprocessing logic.")


        # 최적 카드 선택 (연회비 고려)
        top_cards = select_top_card_with_low_fee(card_scores, card_info)

        # 유사 카드 추천
        recommendations = get_most_similar_cards(top_cards, similarity_df, num_similar=1)
        # 사용자 관심사 기반 혜택 추가
        enriched_recommendations = add_user_interest_to_recommendations(
            recommendations, combined_interest, card_ctg_list, categories_df
        )

        # 광고 생성 및 처리
        ad_results = generate_ads_for_user(enriched_recommendations, card_info)
        processed_ads = process_ad_results(ad_results)

        return jsonify(processed_ads.to_dict(orient="records")), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    # pkl 파일이 존재하지 않으면 한 번만 데이터 준비를 실행
    if not os.path.exists("processed_data.pkl"):
        preprocess_and_save_data()  # 서버 시작 시 한 번만 데이터 준비
    app.run(debug=True)