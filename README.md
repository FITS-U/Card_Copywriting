# LLM 기반 카드 추천 및 광고 생성 시스템
## 프로젝트 개요
이 프로젝트는 사용자 관심도와 카드 혜택 데이터를 기반으로 최적의 카드 추천과 창의적인 광고 문구 생성을 목표로 합니다. Python과 LLM(Large Language Model)을 활용하여 데이터를 분석하고 광고를 제작하며, 사용자 맞춤형 경험을 제공합니다.

## 주요 기능
**1. 카드 추천**
- 사용자 (클릭 로그 데이터 활용) 관심도를 기반으로 카드 점수 계산.
- 사용자의 명시적, 암묵적 관심도를 고려하여 맞춤형 카드 추천.

**2. 광고 문구 생성**

- 추천된 카드를 바탕으로 감성적이고 실용적인 광고 카피 생성.
- 카드의 주요 혜택을 강조하며, 이모티콘을 활용한 생동감 있는 문구 제공.

**3. 유사 카드 추천**

- 벡터화된 카드 데이터를 기반으로 코사인 유사도를 계산하여 가장 유사한 카드 추천.

**4. 데이터 전처리 및 관리**

- 연회비 데이터 전처리, 카드 혜택 데이터 병합.
- .gitignore를 활용하여 민감한 데이터를 보호.


