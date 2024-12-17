import pandas as pd

# 명시적 관심도
def calculate_explicit_interest(categories_df):
    return categories_df.groupby('category_id').size().reset_index(name='explicit_interest')

# 암묵적 관심도
def calculate_implicit_interest(logs_df):
    # logs_df가 비어있으면 빈 DataFrame 반환
    if logs_df.empty:
        return pd.DataFrame(columns=['category_id', 'implicit_interest'])
    return logs_df.groupby('category_id').size().reset_index(name='implicit_interest')


# 명시적/암묵적 관심도 병합
def merge_interests(explicit_interest, implicit_interest):

    # 명시적 관심도와 암묵적 관심도 병합
    combined = pd.merge(explicit_interest, implicit_interest, on=['category_id'], how='outer').fillna(0)

    # 관심 카테고리별 빈도수 계산
    combined['interest_count'] = len(combined['category_id'].unique())
    return combined


def filter_card_benefits_by_user_interest(combined_interest, card_ctg_list):
    
    user_interest_categories = set(combined_interest['category_id'].astype(str))
    
    # 카드별 혜택과 사용자 관심사 교집합 계산 및 필터링
    card_ctg_list['intersection'] = card_ctg_list['category_id'].apply(
        lambda x: list(set(map(str, x.keys() if isinstance(x, dict) else x)) & user_interest_categories)
    )
    return card_ctg_list[card_ctg_list['intersection'].str.len() > 0]
