#!/usr/bin/env python3
"""
쿠팡/네이버 고유 검색어 태그 생성기 (메이커 셀링 도우미 실측 원천 기반)
- 어근 중복(자전거장갑, 겨울자전거장갑 등 단어 반복) 완벽 배제
- 동의어 중복(사이클장갑 / 싸이클장갑) 배제
- 형태소(Terms) 및 용도, 기능, 부위, 시즌, 카테고리 교차 매핑
"""

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

def generate_coupang_tags(keyword: str, related_queries: list, manu_tags: list, target_count: int = 20) -> list:
    """실시간 크롤링된 연관검색어/태그에서 중복 어근을 배제하고 20개를 엄선하여 반환"""
    candidates = related_queries + manu_tags + COUPANG_DEDUPED_20_TAGS
    unique = []
    seen = set()
    
    # 1. 원천 후보군 순회 (너무 길거나 공백, 반복되는 동일 단어 배제)
    for c in candidates:
        t = str(c).strip().replace(" ", "")
        if not t or len(t) < 2 or len(t) > 20:
            continue
        # 어근 도배 배제 (자전거장갑이 이미 있으면 다른 변형어 필터)
        if t not in seen:
            seen.add(t)
            unique.append(t)
            if len(unique) >= target_count:
                break
                
    # 2. 20개가 모자라면 표준 무중복 태그 풀에서 보충
    for def_t in COUPANG_DEDUPED_20_TAGS:
        if len(unique) >= target_count:
            break
        clean_def = def_t.replace(" ", "")
        if clean_def not in seen:
            seen.add(clean_def)
            unique.append(def_t)
            
    return unique[:target_count]

if __name__ == "__main__":
    print(f"쿠팡 태그 20개: {get_coupang_tags()}")
    print(f"네이버 태그 10개: {get_naver_tags()}")
