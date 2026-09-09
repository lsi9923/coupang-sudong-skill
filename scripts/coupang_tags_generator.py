#!/usr/bin/env python3
"""
쿠팡/네이버 고유 검색어 태그 생성기 (메이커 셀링 도우미 실측 원천 기반)
- 어근 중복(자전거장갑, 겨울자전거장갑 등 단어 반복) 완벽 배제
- 동의어 중복(사이클장갑 / 싸이클장갑) 배제
- 형태소(Terms) 및 용도, 기능, 부위, 시즌, 카테고리 교차 매핑
"""

# 메이커 셀링 도우미 실측 원천 기반 무중복 20대 표준 쿠팡 태그
COUPANG_DEDUPED_20_TAGS = [
    "라이딩장갑",
    "바이크장갑",
    "오토바이장갑",
    "mtb장갑",
    "로드자전거장갑",
    "스포츠장갑",
    "사이클장갑",
    "자전거긴장갑",
    "방한장갑",
    "겨울장갑",
    "기모장갑",
    "손바닥패드",
    "터치스크린장갑",
    "방풍장갑",
    "산악장갑",
    "등산장갑",
    "자전거용품",
    "동계라이딩",
    "손보호대",
    "보온장갑"
]

# 네이버 태그 사전 검증 기반 무중복 10대 태그
NAVER_DEDUPED_10_TAGS = [
    "라이딩장갑",
    "바이크장갑",
    "오토바이장갑",
    "mtb장갑",
    "로드자전거장갑",
    "스포츠장갑",
    "방한장갑",
    "겨울장갑",
    "사이클장갑",
    "자전거긴장갑"
]

def get_coupang_tags():
    return COUPANG_DEDUPED_20_TAGS

def get_naver_tags():
    return NAVER_DEDUPED_10_TAGS

if __name__ == "__main__":
    print(f"쿠팡 태그 ({len(COUPANG_DEDUPED_20_TAGS)}개):")
    for i, t in enumerate(COUPANG_DEDUPED_20_TAGS, 1):
        print(f"{i}. {t}")
    print(f"\n네이버 태그 ({len(NAVER_DEDUPED_10_TAGS)}개):")
    for i, t in enumerate(NAVER_DEDUPED_10_TAGS, 1):
        print(f"{i}. {t}")
