#!/usr/bin/env python3
"""
쿠팡 2026 실전 전략(스월백 & 대디갓재) 완벽 통합 파이프라인 검증 테스트
"""
import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts"))
from run_coupang_pipeline import build_coupang_complete_payload

def test_pipeline():
    schema_path = os.path.join(os.path.dirname(__file__), "..", "contracts", "coupang-listing-payload.schema.json")
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
        
    sample = {
        "mainKeyword": "자전거장갑",
        "brand": "G-SPORT",
        "cnyPrice": 8.5,
        "features": ["겨울 방한", "방풍 기모", "터치스크린", "충격흡수"],
        "colors": ["검정색", "회색", "흰색"],
        "sizes": ["남녀공용 프리(Free)"],
        "candidateTags": ["겨울자전거장갑", "라이딩장갑", "방한장갑", "바이크장갑", "오토바이장갑", "로드자전거장갑", "싸이클장갑", "터치장갑", "방풍장갑", "기모장갑", "MTB장갑", "사이클장갑"]
    }
    
    payload = build_coupang_complete_payload(sample, use_free_shipping=True, use_make_order_delay=True)
    
    # 1. 스키마 필수 필드 검증
    for req in schema["required"]:
        assert req in payload, f"Missing required property: {req}"
        
    # 2. [스월백/대디갓재 룰 1] F자 패턴 상품명: 단어 수 5~6개 내외, 메인 키워드 뒷단 배치
    words = payload["sellerProductName"].split()
    assert 3 <= len(words) <= 7, f"Title word count out of bounds: {len(words)} ({payload['sellerProductName']})"
    assert words[-1] == "자전거장갑" or "자전거" in words[-1] or "장갑" in words[-1], "Main keyword must be positioned at the rear (F-pattern)"
    
    # 3. [스월백/대디갓재 룰 2] 색상 표준화: 검정->블랙, 회색->그레이, 흰색->화이트
    colors_in_options = [o["attributes"][0]["attributeValueName"] for o in payload["options"]]
    assert "블랙" in colors_in_options[0]
    assert "그레이" in colors_in_options[1]
    assert "화이트" in colors_in_options[2]
    
    # 4. [스월백/대디갓재 룰 3] 100% 무료배송 전환 & 정상가 분리
    assert payload["deliveryChargeType"] == "FREE"
    assert payload["deliveryCharge"] == 0
    assert payload["originalPrice"] > payload["salePrice"]
    
    # 5. [스월백/대디갓재 룰 4] 주문제작 출고소요일 연장 (패널티 방어)
    assert payload["deliveryMethod"] == "MAKE_ORDER"
    assert payload["outboundShippingTimeDay"] >= 14
    
    # 6. [스월백/대디갓재 룰 5] 태그 20개 빈칸 0개
    assert len(payload["searchTags"]) == 20
    
    # 7. [스월백/대디갓재 룰 6] 고시정보 품명 및 모델명에 [브랜드 + 메인키워드] 가중치 주입
    assert "G-SPORT" in payload["notices"][0]["content"]
    assert "자전거장갑" in payload["notices"][0]["content"]
    
    # 8. [사후관리] 노출 상품 ID 백업 가이드 탑재 확인
    assert "_postRegistrationTips" in payload
    assert "노출 상품 ID" in payload["_postRegistrationTips"]["backupAction"]
    
    print("Coupang Practical Pipeline Verification Passed 100%!")
    print(f"- F자 패턴 상품명 ({len(words)}단어): {payload['sellerProductName']}")
    print(f"- 색상 표준화 성공: {colors_in_options}")
    print(f"- 무료배송 세팅 완료: 판매가 {payload['salePrice']:,}원 (정상가 {payload['originalPrice']:,}원, 배송비 0원)")
    print(f"- 배송지연 패널티 방어: {payload['deliveryMethod']} (출고소요일 {payload['outboundShippingTimeDay']}일)")
    print(f"- 고시 품명및모델명 가중치: {payload['notices'][0]['content']}")
    print(f"- 검색어 태그 20개 풀장착 완료")
    print(f"- 사후관리 노출 상품 ID 백업 가이드 확인")

if __name__ == "__main__":
    test_pipeline()
