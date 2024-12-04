# from data_handler import  preprocess_card_data
# from interest_calculator import (
#     calculate_explicit_interest,
#     calculate_implicit_interest,
#     merge_interests,
# )
# from contents import vectorize_card_data, calculate_card_similarity
# from card_recommendation import (
#     calculate_card_scores,
#     select_top_card_with_low_fee,
#     get_most_similar_cards,
#     add_user_interest_to_recommendations
# )
# from ad_generator import generate_ads_for_user,process_ad_results
# import pandas as pd
# from flask import Flask, jsonify, request
# import logging

# # 로깅 설정
# logging.basicConfig(
#     filename="debug.log",
#     level=logging.DEBUG,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )

# app = Flask(__name__)

# # 글로벌 데이터 저장소
# global_data = {
#     "card_info": None,
#     "card_ctg_list": None,
#     "similarity_df": None,
# }

# # 초기화 함수
# def initialize_global_data():
#     try:
#         # 카드 정보 로드
#         card_info = pd.read_csv("data/카드정보.csv")
#         card_category = pd.read_csv("data/CardCategory.csv")

#         # 카드 데이터 전처리
#         categories_df = pd.read_csv("data/Category.csv")  # 공통 카테고리 데이터
#         card_ctg_list = preprocess_card_data(card_category, categories_df)

#         # 벡터화 및 유사도 계산
#         ctg_matrix, _ = vectorize_card_data(card_ctg_list)
#         similarity_df = calculate_card_similarity(ctg_matrix, card_ctg_list)

#         # 글로벌 데이터 저장
#         global_data.update({
#             "card_info": card_info,
#             "card_ctg_list": card_ctg_list,
#             "similarity_df": similarity_df,
#         })

#         print("Global data initialized successfully!")
#     except Exception as e:
#         logging.error(f"Error during global data initialization: {str(e)}")
#         raise

# # 광고 추천 엔드포인트
# @app.route("/advertisement", methods=["POST"])
# def get_advertisement():
#     try:
#         # 요청 데이터 수신
#         request_data = request.get_json()
#         categories = request_data.get("categories", [])
#         logs = request_data.get("logs", [])
#         category_df = pd.DataFrame(categories)
#         logs_df = pd.DataFrame(logs)

#         # 관심도 계산
#         explicit_interest = calculate_explicit_interest(category_df)
#         implicit_interest = calculate_implicit_interest(logs_df)
#         combined_interest = merge_interests(explicit_interest, implicit_interest)

#         # 카드 점수 계산
#         card_ctg_list = global_data["card_ctg_list"]
#         card_scores = calculate_card_scores(card_ctg_list, combined_interest)

#         # 사용자별 최적 카드 선택
#         top_cards = select_top_card_with_low_fee(card_scores, global_data["card_info"])

#         # 유사 카드 추천
#         similarity_df = global_data["similarity_df"]
#         recommendations = get_most_similar_cards(top_cards, similarity_df, num_similar=2)

#         # 사용자 관심사 기반 혜택 추가
#         categories = pd.read_csv("data/Category.csv")
#         enriched_recommendations = add_user_interest_to_recommendations(
#             recommendations, combined_interest, card_ctg_list, categories
#         )

#         # 광고 생성
#         ad_results = generate_ads_for_user(1, enriched_recommendations, global_data["card_info"])
#         processed_ads = process_ad_results(ad_results)

#         # 결과 반환
#         return jsonify(processed_ads)
#     except Exception as e:
#         logging.error(f"Error processing advertisement: {str(e)}")
#         return jsonify({"error": str(e)}), 500


# if __name__ == "__main__":
#     # 초기화 단계
#     initialize_global_data()

#     # 서버 실행
#     app.run(debug=True)





    ## --------------------------------------여기-- ##
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

# 로깅 설정
logging.basicConfig(
    filename="debug.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# 테스트용 데이터
test_data = {
    "categories": [
        {"categoryId": 8},
        {"categoryId": 9},
        {"categoryId": 18},
        {"categoryId": 26},
        {"categoryId": 29}
    ],
    "logs": [
        {"categoryId": 8, "eventType": "Click", "clickTime": "2024-12-01T15:26:32.843038"},
        {"categoryId": 9, "eventType": "Click", "clickTime": "2024-12-01T15:26:33.561888"},
        {"categoryId": 18, "eventType": "Click", "clickTime": "2024-12-01T15:26:34.259727"},
        {"categoryId": 26, "eventType": "Click", "clickTime": "2024-12-01T15:26:34.259727"},
        {"categoryId": 29, "eventType": "Click", "clickTime": "2024-12-01T15:26:34.259727"}
    ]
}

# 테스트용 Benefit 데이터
import pandas as pd

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


from flask import Flask, jsonify, request
app = Flask(__name__)  # Flask 앱 객체 생성
@app.route('/generate_ads', methods=['POST'])
def generate_ads():
    try:
        # JSON 데이터를 DataFrame으로 변환
        categories = test_data.get("categories", [])
        logs = test_data.get("logs", [])
        category_df = pd.DataFrame(categories)
        logs_df = pd.DataFrame(logs)

        # 관심도 계산
        explicit_interest = calculate_explicit_interest(category_df)
        implicit_interest = calculate_implicit_interest(logs_df)
        combined_interest = merge_interests(explicit_interest, implicit_interest)

        # 카드 데이터 초기화
        card_info = pd.read_csv("data/CardInfo.csv")
        card_info = preprocess_annual_fee(card_info)  # 연회비 전처리

        
        card_category = pd.read_csv("data/CardCategory.csv")
        categories_df = pd.read_csv("data/Category.csv")


        card_ctg_list = preprocess_card_data(card_category, categories_df)
        # 데이터 타입 통일
        card_ctg_list['categoryId'] = card_ctg_list['categoryId'].astype(str)
        combined_interest['categoryId'] = combined_interest['categoryId'].astype(str)


        # 벡터화 및 유사도 계산
        ctg_matrix, _ = vectorize_card_data(card_ctg_list)
        similarity_df = calculate_card_similarity(ctg_matrix, card_ctg_list)

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
    app.run(debug=True)
