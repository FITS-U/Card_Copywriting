# import pandas as pd
# from data_handler import preprocess_card_data,preprocess_annual_fee
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
# from ad_generator import generate_ads_for_user, process_ad_results
# import logging
# from flask import Flask, jsonify, request
# from db import Database

# # 로깅 설정
# logging.basicConfig(
#     level=logging.DEBUG,
# )


# # def data_load():
# #     # 데이터 불러오기
# #     Category=Database()
# #     Category_df = Category.execute("SELECT * FROM Category;")

# #     CardInfo=Database()
# #     CardInfo_df = CardInfo.execute("SELECT * FROM CardInfo;")

# #     Benefit=Database()
# #     Benefit_df = Benefit.execute("SELECT * FROM Benefit;")
# #     Benefit_df = Benefit_df.rename(columns=[{"category_id":'categoryid'},{'card_id':'cardid'}])

# #     print(f"Benefit_df: {Benefit_df}")
# #     print(f"CardInfo_df: {CardInfo_df}")
# #     print(f"Category_df: {Category_df}")
# #     return Category_df, CardInfo_df, Benefit_df

    

# # app = Flask(__name__)  # Flask 앱 객체 생성
# # @app.route('/generate_ads', methods=['POST'])
# # def generate_ads():
# #     try:
# #         # 테스트용 데이터
# #         test_data = {
# #             "category": [
# #                 {"categoryid": 8},
# #                 {"categoryid": 9},
# #                 {"categoryid": 18},
# #                 {"categoryid": 26},
# #                 {"categoryid": 29}
# #             ],
# #             "logs": [
# #                 {"categoryid": 8, "eventType": "Click", "clickTime": "2024-12-01T15:26:32.843038"},
# #                 {"categoryid": 9, "eventType": "Click", "clickTime": "2024-12-01T15:26:33.561888"},
# #                 {"categoryid": 18, "eventType": "Click", "clickTime": "2024-12-01T15:26:34.259727"},
# #                 {"categoryid": 26, "eventType": "Click", "clickTime": "2024-12-01T15:26:34.259727"},
# #                 {"categoryid": 29, "eventType": "Click", "clickTime": "2024-12-01T15:26:34.259727"}
# #             ]
# #         }


# #         # 데이터
# #         card_category, card_info, categories_df = data_load()
# #         benefits = categories_df.groupby('cardid')['benefittitle'].apply(list).reset_index(name='benefits')

# #         categories = test_data.get("category", [])
# #         logs = test_data.get("logs", [])

# #         # JSON 데이터를 DataFrame으로 변환
# #         category_df = pd.DataFrame(categories)
# #         logs_df = pd.DataFrame(logs)

# #         # 관심도 계산
# #         explicit_interest = calculate_explicit_interest(category_df)
# #         implicit_interest = calculate_implicit_interest(logs_df)
# #         combined_interest = merge_interests(explicit_interest, implicit_interest)

# #         card_info = preprocess_annual_fee(card_info)  # 연회비 전처리

# #         card_ctg_list = preprocess_card_data(card_category, categories_df)
# #         # 데이터 타입 통일
# #         card_ctg_list['categoryid'] = card_ctg_list['categoryid'].astype(str)
# #         combined_interest['categoryid'] = combined_interest['categoryid'].astype(str)


# #         # 벡터화 및 유사도 계산
# #         ctg_matrix, _ = vectorize_card_data(card_ctg_list)
# #         similarity_df = calculate_card_similarity(ctg_matrix, card_ctg_list)
# #         print(similarity_df)
# #         # 카드 점수 계산
# #         card_scores = calculate_card_scores(card_ctg_list, combined_interest)
# #         print(card_scores)
# #         # 최적 카드 선택 (연회비 고려)
# #         top_cards = select_top_card_with_low_fee(card_scores, card_info)
# #         print(top_cards)
# #         # 유사 카드 추천
# #         recommendations = get_most_similar_cards(top_cards, similarity_df, num_similar=1)
# #         # 사용자 관심사 기반 혜택 추가
# #         enriched_recommendations = add_user_interest_to_recommendations(
# #             recommendations, combined_interest, card_ctg_list, categories_df
# #         )
# #         # 광고 생성 및 처리
# #         ad_results = generate_ads_for_user(enriched_recommendations, card_info)
# #         processed_ads = process_ad_results(ad_results)


# #         return jsonify(processed_ads.to_dict(orient="records")), 200
# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500

# def data_load():
#     try:
#         print("데이터 불러오기 시작...")

#         # 데이터베이스 연결 및 쿼리 실행
#         Category = Database()
#         Category_df = Category.execute("SELECT * FROM Category;")
#         print(f"Category_df:\n{Category_df.head()}")  # 데이터 출력

#         CardInfo = Database()
#         CardInfo_df = CardInfo.execute("SELECT * FROM CardInfo;")
#         print(f"CardInfo_df:\n{CardInfo_df.head()}")  # 데이터 출력

#         Benefit = Database()
#         Benefit_df = Benefit.execute("SELECT * FROM Benefit;")
#         print(f"Benefit_df 원본:\n{Benefit_df.head()}")  # 원본 데이터 출력

#         # 컬럼 이름 변경
#         Benefit_df = Benefit_df.rename(
#             columns={"category_id": 'categoryid', 'card_id': 'cardid'}
#         )
#         print(f"Benefit_df 리네임 후:\n{Benefit_df.head()}")  # 리네임된 데이터 출력

#         return Category_df, CardInfo_df, Benefit_df

#     except Exception as e:
#         print(f"data_load() 에러 발생: {e}")
#         raise e  # 에러를 다시 발생시켜 상위 코드로 전달

# # app = Flask(__name__)  # Flask 앱 객체 생성
# # @app.route('/generate_ads', methods=['POST'])
# def generate_ads():
#     try:
#         print("테스트 데이터 준비 중...")
#         # 테스트용 데이터
#         test_data = {
#             "category": [
#                 {"categoryid": 8},
#                 {"categoryid": 9},
#                 {"categoryid": 18},
#                 {"categoryid": 26},
#                 {"categoryid": 29}
#             ],
#             "logs": [
#                 {"categoryid": 8, "eventType": "Click", "clickTime": "2024-12-01T15:26:32.843038"},
#                 {"categoryid": 9, "eventType": "Click", "clickTime": "2024-12-01T15:26:33.561888"},
#                 {"categoryid": 18, "eventType": "Click", "clickTime": "2024-12-01T15:26:34.259727"},
#                 {"categoryid": 26, "eventType": "Click", "clickTime": "2024-12-01T15:26:34.259727"},
#                 {"categoryid": 29, "eventType": "Click", "clickTime": "2024-12-01T15:26:34.259727"}
#             ]
#         }
#         print("테스트 데이터 준비 완료.")

#         print("데이터 로드 시작...")
#         card_category, card_info, categories_df = data_load()
#         print("데이터 로드 완료.")

#         print("카테고리 데이터프레임 생성 중...")
#         benefits = categories_df.groupby('cardid')['benefittitle'].apply(list).reset_index(name='benefits')
#         print("카테고리 데이터프레임 생성 완료.")

#         categories = test_data.get("category", [])
#         logs = test_data.get("logs", [])

#         print("JSON 데이터를 DataFrame으로 변환 중...")
#         category_df = pd.DataFrame(categories)
#         logs_df = pd.DataFrame(logs)
#         print("DataFrame 변환 완료.")

#         print("관심도 계산 시작...")
#         explicit_interest = calculate_explicit_interest(category_df)
#         implicit_interest = calculate_implicit_interest(logs_df)
#         combined_interest = merge_interests(explicit_interest, implicit_interest)
#         print("관심도 계산 완료.")

#         print("연회비 전처리 중...")
#         card_info = preprocess_annual_fee(card_info)

#         print("카드 데이터 전처리 시작...")
#         card_ctg_list = preprocess_card_data(card_category, categories_df)
#         print("카드 데이터 전처리 완료.")

#         print("데이터 타입 통일 중...")
#         card_ctg_list['categoryid'] = card_ctg_list['categoryid'].astype(str)
#         combined_interest['categoryid'] = combined_interest['categoryid'].astype(str)
#         print("데이터 타입 통일 완료.")

#         print("벡터화 및 유사도 계산 중...")
#         ctg_matrix, _ = vectorize_card_data(card_ctg_list)
#         similarity_df = calculate_card_similarity(ctg_matrix, card_ctg_list)
#         print(similarity_df)
#         print("유사도 계산 완료.")

#         print("카드 점수 계산 시작...")
#         card_scores = calculate_card_scores(card_ctg_list, combined_interest)
        
#         print(card_scores)
#         print("카드 점수 계산 완료.")

#         print("최적 카드 선택 중...")
#         top_cards = select_top_card_with_low_fee(card_scores, card_info)
#         print(top_cards)
#         print("최적 카드 선택 완료.")

#         print("유사 카드 추천 시작...")
#         recommendations = get_most_similar_cards(top_cards, similarity_df, num_similar=1)

#         print("사용자 관심사 기반 혜택 추가 중...")
#         enriched_recommendations = add_user_interest_to_recommendations(
#             recommendations, combined_interest, card_ctg_list, card_category
#         )

#         print("광고 생성 및 처리 중...")
#         ad_results = generate_ads_for_user(enriched_recommendations, card_info)
#         processed_ads = process_ad_results(ad_results)

#         print(enriched_recommendations)

#     except Exception as e:
#         print(f"에러 발생: {e}")

# if __name__ == '__main__':
#     # app.run(host='0.0.0.0', port=5000, debug=True)
#     generate_ads()


# ------ 

import pandas as pd
from flask import Flask, jsonify, request
import requests
from data_handler import preprocess_card_data, preprocess_annual_fee
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
from db import Database
import logging
import json
# 로깅 설정
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# 데이터 로드 함수
def data_load():
    try:
        logging.debug("데이터 불러오기 시작...")
        Category = Database()
        Category_df = Category.execute("SELECT * FROM Category;")

        CardInfo = Database()
        CardInfo_df = CardInfo.execute("SELECT * FROM CardInfo;")

        Benefit = Database()
        Benefit_df = Benefit.execute("SELECT * FROM Benefit;")
        Benefit_df = Benefit_df.rename(columns={"category_id": 'categoryid', 'card_id': 'cardid'})

        logging.debug("데이터 로드 완료.")
        return Category_df, CardInfo_df, Benefit_df
    except Exception as e:
        logging.error(f"데이터 로드 중 에러 발생: {e}")
        raise

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Ads API"}), 200

@app.route('/favicon.ico')
def favicon():
    return "", 204  # No Content

@app.route('/generate_ads', methods=['POST'])
def generate_ads():
    try:
        # 테스트 데이터 수신
        test_data = request.get_json("http://192.168.1.4:8091/api/v1/advertisement")
        # 요청이 성공했는지 확인
        if not test_data:
            return jsonify({"error": "Invalid input data"}), 400
        
        logging.debug("입력 데이터 수신 완료.")

        # 데이터 로드
        card_category, card_info, categories_df = data_load()

        # 혜택 데이터 생성
        benefits = categories_df.groupby('cardid')['benefittitle'].apply(list).reset_index(name='benefits')

        categories = test_data.get("category", [])
        logs = test_data.get("logs", [])

        # JSON 데이터를 DataFrame으로 변환
        category_df = pd.DataFrame(categories)
        logs_df = pd.DataFrame(logs)

        # 관심도 계산
        explicit_interest = calculate_explicit_interest(category_df)
        implicit_interest = calculate_implicit_interest(logs_df)
        combined_interest = merge_interests(explicit_interest, implicit_interest)

        # 연회비 및 카드 데이터 전처리
        card_info = preprocess_annual_fee(card_info)
        card_ctg_list = preprocess_card_data(card_category, categories_df)

        # 데이터 타입 통일
        card_ctg_list['categoryid'] = card_ctg_list['categoryid'].astype(str)
        combined_interest['categoryid'] = combined_interest['categoryid'].astype(str)

        # 벡터화 및 유사도 계산
        ctg_matrix, _ = vectorize_card_data(card_ctg_list)
        similarity_df = calculate_card_similarity(ctg_matrix, card_ctg_list)

        # 카드 점수 계산
        card_scores = calculate_card_scores(card_ctg_list, combined_interest)

        # 최적 카드 선택 (연회비 고려)
        top_cards = select_top_card_with_low_fee(card_scores, card_info)

        # 유사 카드 추천
        recommendations = get_most_similar_cards(top_cards, similarity_df, num_similar=1)

        # 사용자 관심사 기반 혜택 추가
        enriched_recommendations = add_user_interest_to_recommendations(
            recommendations, combined_interest, card_ctg_list, card_category
        )
        # 광고 생성 및 처리
        ad_results = generate_ads_for_user(enriched_recommendations, card_info)
        processed_ads = process_ad_results(ad_results)
        ad_data = processed_ads.to_dict(orient="records")
        
        print(ad_data)
        
        return jsonify(ad_data), 200

    except Exception as e:
        logging.error(f"에러 발생: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
