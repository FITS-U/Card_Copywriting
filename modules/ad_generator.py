import os
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import pandas as pd
from dotenv import load_dotenv
import json
from flask import jsonify

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")


# 광고 문구 생성 함수
def generate_advertising_copy(benefits):
    # LLM 모델 설정
    llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0.7,
            streaming=True)

    # 프롬프트 템플릿
    prompt_template = """
        당신은 창의적이고 재능 있는 광고 카피라이터입니다. 

        - 카드 혜택을 바탕으로 서로 다른 스타일의 광고 문구를 작성하세요.
        - 각각의 광고 문구는 독립적이며 서로 다른 접근 방식으로 작성되어야 합니다.
        - 이모티콘을 사용해 생동감을 더하고, 간결하면서도 직관적으로 전달되도록 하세요.
        - 광고를 두 줄로 작성하세요.
        - 반드시 JSON 형식으로만 답변하세요. 다음과 같은 형식을 무조건 따르세요:
        {{
            "adCopy1": "첫 번째 줄의 문구",
            "adCopy2": "두 번째 줄의 문구"
        }}

        ### 카드 정보:
        - 혜택: {benefits}

        ### 참고 예시:
        광고 문구는 아래의 서로 다른 스타일을 참고하여 작성하세요:
        1.
            {{
            "adCopy1" : "맛있는 외식과 즐거운 쇼핑이 당신을 기다려요! 🍽️🛍️",
            "adCopy2" : "특별한 순간을 더욱 특별하게 만들어줄 카드와 함께하세요! ✨💖"
            }}
        2.
            {{
            "adCopy1" : "외식비는 줄이고, 쇼핑 포인트는 더하세요! 💳💰",
            "adCopy2" : "알뜰한 소비, 더 행복한 일상을 만드는 카드! 🛍️🌟"
            }}
       
        작성할 문구 :
        
        """
    # 프롬프트 생성 및 실행
    prompt = PromptTemplate(template=prompt_template)
    llm_chain = prompt | llm
    formatted_input = {"benefits": benefits}
    response = llm_chain.invoke(formatted_input)
    return json.loads(response.content)


def generate_ads_for_user(filtered_recommendations, card_info):
    # 추천 카드 상위 2개 선택
    top_recommendations = filtered_recommendations.head(2)

    merged_data = top_recommendations.merge(card_info,
                                            left_on="final_card",
                                            right_on="card_id",
                                            how="inner")
    ad_results = []

    for _, row in merged_data.iterrows():
        ad_copy = generate_advertising_copy(row["ctg_name_list"])
        ad_results.append({
            "card_id":row["final_card"],
            "card_name": row["card_name"],
            "adCopy1":ad_copy.get("adCopy1",""),
            "adCopy2":ad_copy.get("adCopy2",""),
            "image_url":row["image_url"]
        })

    return jsonify(ad_results),200


