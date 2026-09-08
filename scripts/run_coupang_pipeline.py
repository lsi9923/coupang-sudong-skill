#!/usr/bin/env python3
"""
쿠팡 윙 상위노출 수동등록 4단계 완벽 통합 파이프라인 (스월백 & 대디갓재 2026 실전 전략 완벽 통합)
1. 노출 상품명: [브랜드] + [고관여 소구점] + [메인키워드] F자 시선 패턴 (5~6단어 제한, 특수기호/옵션단어 제거)
2. 20개 검색어 태그: 자동완성/연관검색어 20개 풀장착 (빈자리 0개)
3. 카테고리 & 속성: 쿠팡 실제 좌측 사이드바 필터 1:1 매칭 + 색상 표준명(화이트/그레이/블랙) 변환
4. 고시정보: '품명 및 모델명'에 [브랜드 + 메인키워드] 주입하여 검색 가중치 추가 획득
5. 배송 전략: 100% 무료배송 전환 (배송비 판매가 녹임) + 주문제작(MAKE_ORDER) 출고소요일 최대 20일 연장 지원
6. 사후 관리: 노출 상품 ID 사전 백업 가이드 자동 출력
"""
import argparse
import json
import sys
from pathlib import Path

from coupang_title_composer import compose_coupang_f_pattern_title
from coupang_tags_generator import generate_coupang_tags
from coupang_category_matcher import match_coupang_category_and_notices, normalize_coupang_color

def build_coupang_complete_payload(
    sourcing_spec: dict,
    seller_config: dict | None = None,
    use_free_shipping: bool = True,
    use_make_order_delay: bool = True
) -> dict:
    if seller_config is None:
        seller_config = {
            "vendorId": "A00123456",
            "deliveryCompanyCode": "CJGLS",
            "outboundShippingPlaceCode": 10001,
            "returnCenterCode": 20001,
            "returnAddress": "인천광역시 검단구 완정로 146 (리더스빌) 2층 208-43c호 (23466)",
            "companyContactNumber": "010-0000-0000"
        }

    main_keyword = sourcing_spec.get("mainKeyword", "자전거장갑")
    brand = sourcing_spec.get("brand", "")
    
    # 1. 카테고리 메타데이터 및 고시/속성 매칭
    cat_meta = match_coupang_category_and_notices(main_keyword, brand or "자체제작")
    
    # 2. [상품명] F자 시선 패턴 5~6단어 고밀도 조합
    features = sourcing_spec.get("features", ["겨울 방한", "방풍 기모", "터치스크린"])
    seller_product_name = compose_coupang_f_pattern_title(brand, main_keyword, features, max_words=6)
    display_product_name = f"{brand} {seller_product_name}".strip()[:100]
    
    # 3. [검색어 태그] 20개 빈칸 0개 풀장착
    search_tags = generate_coupang_tags(
        main_keyword,
        sourcing_spec.get("candidateTags", []),
        [cat_meta.get("categoryName", "").split(" > ")[-1]],
        target_count=20
    )
    
    # 4. [가격 및 배송 전략] 100% 무료배송 전환 (배송비 녹임)
    cny_price = sourcing_spec.get("cnyPrice", 8.5)
    exchange_rate = 200
    cost_krw = cny_price * exchange_rate
    shipping_cost = 3500
    margin_rate = 0.35
    
    # 100% 무료배송 전략: 배송비를 판매가에 가산하여 무료배송으로 등록 -> 전환율 & 노출점수 극대화
    if use_free_shipping:
        calculated_sale_price = int(round(((cost_krw + shipping_cost) / (1 - margin_rate)) / 100) * 100)
        delivery_charge_type = "FREE"
        delivery_charge = 0
    else:
        calculated_sale_price = int(round((cost_krw / (1 - margin_rate)) / 100) * 100)
        delivery_charge_type = "NOT_FREE"
        delivery_charge = shipping_cost
        
    # 할인율 20~25% 배지를 위한 정상가 분리 설정
    original_price = int(round((calculated_sale_price * 1.25) / 100) * 100)
    
    # 5. [출고 지연 리스크 방어] 배송 방식 & 출고소요일
    if use_make_order_delay:
        # 해외 수입/로켓그로스 전환 대기 시 주문제작(MAKE_ORDER)으로 최대 20일 출고소요일 확보
        delivery_method = "MAKE_ORDER"
        outbound_days = 14  # 안전권 14일
    else:
        delivery_method = "AGENT_BUY"
        outbound_days = 7
        
    # 6. [옵션 표준화] 색상 명칭 쿠팡 표준화 (흰색->화이트, 회색->그레이)
    raw_colors = sourcing_spec.get("colors", ["블랙", "그레이"])
    normalized_colors = [normalize_coupang_color(c) for c in raw_colors]
    sizes = sourcing_spec.get("sizes", ["남녀공용 프리(Free)"])
    
    options = []
    for c in normalized_colors:
        for s in sizes:
            item_name = f"{seller_product_name} {c} {s}"[:150].strip()
            options.append({
                "itemName": item_name,
                "salePrice": calculated_sale_price,
                "originalPrice": original_price,
                "maximumBuyCount": 999,
                "attributes": [
                    {"attributeTypeName": "색상", "attributeValueName": c},
                    {"attributeTypeName": "사이즈", "attributeValueName": s}
                ]
            })
            
    # 7. 고시정보 항목 구성
    notices = [
        {
            "noticeCategoryName": cat_meta["noticeCategoryName"],
            "noticeCategoryDetailName": n["name"],
            "content": n["value"]
        }
        for n in cat_meta["notices"]
    ]
    
    payload = {
        "displayCategoryCode": cat_meta["displayCategoryCode"],
        "sellerProductName": seller_product_name,
        "displayProductName": display_product_name,
        "generalProductName": main_keyword,
        "brand": brand if brand else "자체제작",
        "manufacture": sourcing_spec.get("manufacturer", "협력업체"),
        "modelName": sourcing_spec.get("modelName", f"{brand} {main_keyword}".strip()),
        "salePrice": calculated_sale_price,
        "originalPrice": original_price,
        "stockQuantity": 999,
        "maximumBuyForPerson": 0,
        "adultOnly": "EVERYONE",
        "taxType": "TAX",
        "deliveryMethod": delivery_method,
        "deliveryCompanyCode": seller_config["deliveryCompanyCode"],
        "deliveryChargeType": delivery_charge_type,
        "deliveryCharge": delivery_charge,
        "outboundShippingTimeDay": outbound_days,
        "pccNeeded": True,
        "overseasPurchased": "OVERSEAS_PURCHASED",
        "emptyBarcode": True,
        "emptyBarcodeReason": "해외구매대행 상품으로 바코드가 없습니다.",
        "searchTags": search_tags,
        "options": options,
        "images": {
            "representative": sourcing_spec.get("repImage", "https://example.com/rep.jpg"),
            "details": sourcing_spec.get("detailImages", ["https://example.com/d1.jpg"])[:9]
        },
        "notices": notices,
        "attributes": cat_meta["attributes"],
        "contents": sourcing_spec.get("detailHtml", "<div style='max-width:860px;'>상세설명</div>"),
        "returns": {
            "returnCharge": 3500,
            "returnShippingCharge": 7000,
            "returnAddress": seller_config["returnAddress"]
        },
        "_postRegistrationTips": {
            "backupAction": "등록 완료 즉시 [상품관리 > 상품조회]에서 부여된 '노출 상품 ID'를 별도 시트에 복사/백업하세요.",
            "recoveryAction": "추후 상품명/태그 수정으로 트래픽이 끊기거나 노출이 누락될 경우 쿠팡 1:1 온라인 문의로 기존 노출 상품 ID 복원을 요청하면 즉시 회복됩니다."
        }
    }
    
    return payload

if __name__ == "__main__":
    sample = {
        "mainKeyword": "자전거장갑",
        "brand": "G-SPORT",
        "cnyPrice": 8.5,
        "colors": ["검정색", "회색", "흰색"],
        "sizes": ["남녀공용 프리(Free)"],
        "candidateTags": ["겨울자전거장갑", "라이딩장갑", "방한장갑", "바이크장갑", "오토바이장갑", "로드자전거장갑", "싸이클장갑", "터치장갑", "방풍장갑", "기모장갑", "MTB장갑"]
    }
    res = build_coupang_complete_payload(sample)
    print(f"F자 패턴 상품명: {res['sellerProductName']} (단어수: {len(res['sellerProductName'].split())})")
    print(f"옵션 색상 표준화: {[o['attributes'][0]['attributeValueName'] for o in res['options']]}")
    print(f"배송/가격: {res['deliveryChargeType']} (판매가 {res['salePrice']}원 / 정상가 {res['originalPrice']}원)")
    print(f"배송방식/출고일: {res['deliveryMethod']} ({res['outboundShippingTimeDay']}일)")
    print(f"고시정보 품명및모델명: {res['notices'][0]['content']}")
    print(f"사후관리 팁: {res['_postRegistrationTips']['backupAction']}")
