import pandas as pd
import re
from modules.interest_calculator import filter_card_benefits_by_user_interest


# 연회비 데이터에서 국내 연회비 추출
def extract_domestic_fee(fee_string):
    match = re.search(r'국내 (?:(\d+)만)?(\d*)천?원?', fee_string)
    if match:
        ten_thousand = int(match.group(1)) * 10000 if match.group(1) else 0
        thousand = int(match.group(2)) * 1000 if match.group(2) else 0
        return ten_thousand + thousand
    return 0

# 연회비 데이터 전처리
def preprocess_annual_fee(annual_fee_data):
    annual_fee_data['domestic_fee'] = annual_fee_data["annual_fee"].apply(extract_domestic_fee)
    return annual_fee_data


# 카드와 대분류 데이터 병합 및 전처리
def preprocess_card_data(card_category, categories_df):
    # 카드 데이터와 대분류 데이터 병합
    card = pd.merge(card_category, categories_df, how='left', on='category_id')

    # 중복된 category_id 지우기
    card.drop_duplicates(subset=['card_id','category_id'],ignore_index=True,inplace=True)

    # 카드별 categoryName categoryid 리스트 생성
    card_ctg_list = card.groupby('card_id').agg({
        'category_id': list,
        'category_name': list
    }).reset_index()
    
    # 리스트 데이터를 문자열로 변환
    card_ctg_list['ctg_name_list'] = card_ctg_list['category_name'].apply(lambda x: " ".join(x))
    
    return card_ctg_list

# 카드 혜택과 사용자 관심 병합
def get_filtered_card_data(user_id, combined_interest, card_ctg_list):
    filtered_cards = filter_card_benefits_by_user_interest(user_id, combined_interest, card_ctg_list)

    # 카드 ID, 이름, 혜택 필드만 유지
    filtered_cards = filtered_cards[['card_id', 'ctg_name_list']]
    return filtered_cards
