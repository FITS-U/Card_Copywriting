import pandas as pd
from flask import Flask, jsonify, request
from modules.data_handler import preprocess_card_data, preprocess_annual_fee
from modules.interest_calculator import (
    calculate_explicit_interest,
    calculate_implicit_interest,
    merge_interests,
)
from modules.contents import tokenized_vectorize_cosine
from modules.card_recommendation import (
    calculate_card_scores,
    select_top_card_with_low_fee,
    get_most_similar_cards,
    add_user_interest_to_recommendations
)
from modules.ad_generator import generate_ads_for_user
from database.db import Database
import logging

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# 전역 변수 선언
card_info = None
card_ctg_list = None
similarity_df = None
card_category = None

# 데이터 로드 함수
def data_load():
    Category = Database()
    Category_df = Category.execute("SELECT * FROM category;")

    CardInfo = Database()
    CardInfo_df = CardInfo.execute("SELECT * FROM card_info;")

    Benefit = Database()
    Benefit_df = Benefit.execute("SELECT * FROM benefit;")

    return Category_df, CardInfo_df, Benefit_df


def _setup():
    global card_info, card_ctg_list, similarity_df, card_category

    # 데이터 로드
    card_category, card_info_df, categories_df = data_load()

    # 연회비 및 카드 데이터 전처리
    card_info = preprocess_annual_fee(card_info_df)
    card_ctg_list = preprocess_card_data(card_category, categories_df)

    # 벡터화 및 유사도 계산
    similarity_df= tokenized_vectorize_cosine(card_ctg_list)

_setup()


@app.route('/generate_ads', methods=['POST'])
def generate_ads():
    try:
        test_data = request.json

        # 혜택 데이터 생성
        categories = test_data.get("category", [])
        logs = test_data.get("logs", [])

        # JSON 데이터를 DataFrame으로 변환
        category_df = pd.DataFrame(categories)
        logs_df = pd.DataFrame(logs)

        # 관심도 계산
        explicit_interest = calculate_explicit_interest(category_df)
        implicit_interest = calculate_implicit_interest(logs_df)
        combined_interest = merge_interests(explicit_interest, implicit_interest)
        # 카드 점수 계산
        card_scores = calculate_card_scores(card_ctg_list, combined_interest)
        # 최적 카드 선택 (연회비 고려)
        top_cards = select_top_card_with_low_fee(card_scores, card_info)

        # 유사 카드 추천
        recommendations = get_most_similar_cards(top_cards, similarity_df, num_similar=2)

        # 사용자 관심사 기반 혜택 추가
        enriched_recommendations = add_user_interest_to_recommendations(
            recommendations, combined_interest, card_ctg_list, card_category
        )

        # 광고 생성 및 처리
        ad_results = generate_ads_for_user(enriched_recommendations, card_info)
        return ad_results

    except Exception as e:
        logging.error(f"에러 발생: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3434, debug=True)
