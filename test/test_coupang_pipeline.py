#!/usr/bin/env python3
"""
쿠팡 10대 핵심 카테고리 전수 동적 파이프라인 검증 테스트
"""
import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts"))
from run_coupang_pipeline import build_coupang_complete_payload

TEST_10_ITEMS = [
    {"mainKeyword": "방한 자전거 장갑", "brand": "G-SPORT", "expectedGroup": "패션잡화"},
    {"mainKeyword": "무선 블루투스 이어폰", "brand": "SOUND-PRO", "expectedGroup": "소형가전"},
    {"mainKeyword": "스테인리스 대용량 텀블러", "brand": "ECO-CUP", "expectedGroup": "주방용품"},
    {"mainKeyword": "오버핏 기모 후드티", "brand": "URBAN-FIT", "expectedGroup": "패션의류"},
    {"mainKeyword": "접이식 릴렉스 캠핑체어", "brand": "OUTDOOR-X", "expectedGroup": "가구캠핑"},
    {"mainKeyword": "히알루론산 수분크림", "brand": "DERMA-LAB", "expectedGroup": "화장품"},
    {"mainKeyword": "3단 수압상승 필터 샤워헤드", "brand": "AQUA-CLEAN", "expectedGroup": "생활욕실"},
    {"mainKeyword": "슬로우 피더 강아지 식기", "brand": "PET-CARE", "expectedGroup": "반려동물"},
    {"mainKeyword": "차량용 15W 맥세이프 거치대", "brand": "CAR-TECH", "expectedGroup": "차량용품"},
    {"mainKeyword": "홈트 라텍스 튜빙밴드 세트", "brand": "FIT-PRO", "expectedGroup": "스포츠헬스"}
]

def test_10_categories_full_pipeline():
    schema_path = os.path.join(os.path.dirname(__file__), "..", "contracts", "coupang-listing-payload.schema.json")
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    for idx, item in enumerate(TEST_10_ITEMS, 1):
        payload = build_coupang_complete_payload(item)
        
        # 1. 스키마 필수 필드 충족 검증
        for req in schema["required"]:
            assert req in payload, f"[{item['mainKeyword']}] Missing required property: {req}"
            
        # 2. 카테고리 매칭 검증
        assert payload["matchedCategoryGroup"] == item["expectedGroup"], f"Category mismatch: {payload['matchedCategoryGroup']} != {item['expectedGroup']}"
        
        # 3. 고시 항목 수 및 '상세페이지 참조' 0건 검증
        assert len(payload["notices"]) >= 8, f"Notices count too small for {item['mainKeyword']}"
        for n in payload["notices"]:
            assert n["content"].strip() != "", f"Empty notice in {item['mainKeyword']}"
            assert "상세페이지 참조" != n["content"].strip(), f"Placeholder '상세페이지 참조' found in {n['noticeCategoryDetailName']}"

        # 4. 필수 속성 매핑 검증
        assert len(payload["attributes"]) >= 4, f"Attributes count too small for {item['mainKeyword']}"
        
        # 5. 태그 20개 검증
        assert len(payload["searchTags"]) == 20
        
        print(f"[{idx}/10 통과] {item['mainKeyword']} -> {payload['matchedCategoryGroup']} (고시 {len(payload['notices'])}개, 속성 {len(payload['attributes'])}개, 인증 {payload['certificationType']})")

    print("\n10대 카테고리 전수 동적 분기 파이프라인 검증 100% 성공!")

if __name__ == "__main__":
    test_10_categories_full_pipeline()
