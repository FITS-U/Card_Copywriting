import os
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")


# 광고 문구 생성 함수
def generate_advertising_copy(card_name, benefits):
    print(f"Generating ad copy for: {card_name} with benefits: {benefits}")
    
    try:
        # LLM 모델 설정
        llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0.7,
            streaming=True
        )

        # 프롬프트 템플릿
        prompt_template = """
        당신은 뛰어난 광고 카피라이터입니다. 카드 이름과 혜택을 바탕으로 카드의 매력을 전달하는 창의적이고 감동적인 카피를 제작하세요.
        - 카드의 혜택을 강조하고, 실용적이거나 감성적인 접근으로 사용자의 관심을 끌어야 합니다.
        - 다양한 스타일로 접근하세요: 예를 들어, 한 문구는 즐겁고 감동적인 톤으로, 다른 문구는 실용적이고 간결한 톤으로 작성해 주세요.
        - 이모티콘으로 생동감을 더하고 직관적으로 전달되도록 하세요.
        - 두 줄로 분량 제한하고, 각 줄은 엔터 처리로 분리
        - 반드시 지시사항을 따르며, 지침을 어길 경우 작업은 실패로 간주됩니다.
        카드 정보:
        - 이름: {card_name}
        - 혜택: {benefits}

        작성할 문구:    
        """
        # 프롬프트 생성 및 실행
        prompt = PromptTemplate(template=prompt_template)
        llm_chain = prompt | llm
        formatted_input = {"card_name": card_name, "benefits": benefits}
        response = llm_chain.invoke(formatted_input)

        return str(response.content)

    except Exception as e:
        print(f"Error generating ad copy: {e}")
        return "Sorry, unable to generate ad copy at this time."




def generate_ads_for_user(filtered_recommendations, card_info):
    # 추천 카드 상위 2개 선택
    top_recommendations = filtered_recommendations.head(2)
    ad_results = []
    for _, row in top_recommendations.iterrows():
        card_id = row['final_card']
        benefits = row['mainCtgNameListStr']

        # 카드 이름 가져오기
        card_name = card_info[card_info['cardId'] == card_id]['cardName']

        # 광고 문구 생성
        ad_copy = generate_advertising_copy(card_name, benefits)

        # 광고 결과 저장
        ad_results.append({
            "cardId": card_id,
            "cardName": card_name,
            "benefits": benefits,
            "adCopy": ad_copy
        })

    return pd.DataFrame(ad_results)




# 광고 결과 처리
def process_ad_results(ad_results):
    processed_results = []

    for _, ad in ad_results.iterrows():
        # adCopy를 두 줄로 나누기
        ad_copy_content = ad["adCopy"].split("\n")
        ad_copy_1 = ad_copy_content[0].strip() if len(ad_copy_content) > 0 else ""
        ad_copy_2 = ad_copy_content[1].strip() if len(ad_copy_content) > 1 else ""

        # 새로운 구조로 저장
        processed_results.append({
            "cardId": ad['cardId'],
            "adCopy1": ad_copy_1,
            "adCopy2": ad_copy_2
        })

    return pd.DataFrame(processed_results)
