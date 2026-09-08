#!/usr/bin/env python3
"""
쿠팡 20개 검색어 태그 생성기
쿠팡 상한: 최대 20개 (각 20자 이내).
빈자리 없이 정확히 20개를 풀장착하여 롱테일 검색 노출을 극대화한다.
"""

def generate_coupang_tags(
    main_keyword: str,
    keywords_pool: list[str],
    category_terms: list[str],
    target_count: int = 20
) -> list[str]:
    combined = [main_keyword] + keywords_pool + category_terms
    
    unique_tags = []
    seen = set()
    
    for k in combined:
        clean = k.strip().replace("  ", " ")
        if not clean:
            continue
        if len(clean) > 20:
            clean = clean[:20].strip()
        if clean not in seen and len(clean) >= 2:
            seen.add(clean)
            unique_tags.append(clean)
            if len(unique_tags) == target_count:
                break
                
    # 만약 20개 미만이면 파생 키워드로 20개를 채움
    modifiers = ["추천", "인기", "전문", "가성비", "고급", "신형", "데일리", "필수템"]
    idx = 0
    while len(unique_tags) < target_count and idx < len(modifiers):
        cand = f"{main_keyword} {modifiers[idx]}"
        if len(cand) <= 20 and cand not in seen:
            seen.add(cand)
            unique_tags.append(cand)
        idx += 1
        
    return unique_tags[:target_count]

if __name__ == "__main__":
    tags = generate_coupang_tags(
        "자전거장갑",
        ["겨울자전거장갑", "라이딩장갑", "방한장갑", "바이크장갑", "오토바이장갑", "로드자전거장갑", "싸이클장갑", "자전거반장갑", "터치장갑", "방풍장갑", "기모장갑", "MTB장갑", "사이클장갑"],
        ["스포츠", "레저", "자전거용품", "라이딩용품", "손보호", "동계라이딩", "보온장갑"]
    )
    print(f"태그 개수: {len(tags)}개")
    for i, t in enumerate(tags, 1):
        print(f"{i}. {t}")
