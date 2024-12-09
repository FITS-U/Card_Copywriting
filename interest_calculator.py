import pandas as pd

# 명시적 관심도 계산
def calculate_explicit_interest(categories_df):
    # categories_df에서 categoryid의 개수를 세어 명시적 관심도 계산
    return categories_df.groupby('categoryid').size().reset_index(name='explicit_interest')

# 암묵적 관심도 계산
def calculate_implicit_interest(logs_df):
    # logs_df에서 Click 이벤트 기반으로 암묵적 관심도 계산
    return logs_df[logs_df['eventType'] == "Click"].groupby('categoryid').size().reset_index(name='implicit_interest')


# 명시적/암묵적 관심도 병합
def merge_interests(explicit_interest, implicit_interest):
    # categoryid 타입 통일
    explicit_interest['categoryid'] = explicit_interest['categoryid'].astype(str)
    implicit_interest['categoryid'] = implicit_interest['categoryid'].astype(str)

    # 명시적 관심도와 암묵적 관심도 병합
    combined = pd.merge(explicit_interest, implicit_interest, on=['categoryid'], how='outer').fillna(0)
    # 데이터 타입 변환
    combined['explicit_interest'] = combined['explicit_interest'].astype(int)
    combined['implicit_interest'] = combined['implicit_interest'].astype(int)

    # 관심 카테고리별 빈도수 계산
    unique_categories_count = len(combined['categoryid'].unique())
    combined['interest_count'] = unique_categories_count    
    return combined


def filter_card_benefits_by_user_interest(combined_interest, card_ctg_list):
    # 전체 사용자 관심 카테고리 추출
    user_interest_categories = set(combined_interest['categoryid'].astype(str)) # set으로 변환

    
    # 카드별 혜택에서 사용자 관심 카테고리와의 교집합 계산
    card_ctg_list = card_ctg_list.copy()  # 복사본 생성
    # categoryid 결측값(NaN)을 빈 리스트로 처리
    card_ctg_list['categoryid'] = card_ctg_list['categoryid'].apply(
        lambda x: [] if pd.isna(x) else x
    )
    
    # categoryid 데이터가 dict일 경우 keys()를 사용해 처리
    card_ctg_list['categoryid'] = card_ctg_list['categoryid'].apply(
        lambda x: set(map(str, x.keys())) if isinstance(x, dict) else set(map(str, x))
    )
    
    # 교집합 계산
    card_ctg_list['intersection'] = card_ctg_list['categoryid'].apply(
        lambda categories: list(categories & user_interest_categories)
    )
    
    # 교집합이 비어있지 않은 카드만 필터링
    filtered_cards = card_ctg_list[card_ctg_list['intersection'].apply(len) > 0]
    
    # 결과 반환
    return filtered_cards
