#!/usr/bin/env python3
"""
쿠팡 윙 상위노출 수동등록 4단계 완벽 통합 파이프라인 (스월백 & 대디갓재 & 메이커 도우미 실전 무중복 태그 통합)
"""
import json
from coupang_title_composer import compose_coupang_f_pattern_title
from coupang_tags_generator import get_coupang_tags
from coupang_category_matcher import match_coupang_category_and_notices, normalize_coupang_color
from genuine_notices_builder import get_coupang_genuine_notices

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
    
    # 1. 카테고리 메타데이터
    cat_meta = match_coupang_category_and_notices(main_keyword, brand or "자체제작")
    
    # 2. [상품명] F자 시선 패턴 5~6단어 고밀도 조합 (특수기호/옵션단어 삭제)
    features = sourcing_spec.get("features", ["겨울 방한", "방풍 기모", "터치스크린"])
    seller_product_name = compose_coupang_f_pattern_title(brand, main_keyword, features, max_words=6)
    display_product_name = f"{brand} {seller_product_name}".strip()[:100]
    
    # 3. [검색어 태그] 메이커 셀링 도우미 실측 원천 기반 중복 0% 20개 풀장착
    search_tags = get_coupang_tags()
    
    # 4. [가격 및 배송 전략] 100% 무료배송 전환 (배송비 판매가 녹임)
    cny_price = sourcing_spec.get("cnyPrice", 8.5)
    exchange_rate = 200
    cost_krw = cny_price * exchange_rate
    shipping_cost = 3500
    margin_rate = 0.35
    
    if use_free_shipping:
        calculated_sale_price = int(round(((cost_krw + shipping_cost) / (1 - margin_rate)) / 100) * 100)
        delivery_charge_type = "FREE"
        delivery_charge = 0
    else:
        calculated_sale_price = int(round((cost_krw / (1 - margin_rate)) / 100) * 100)
        delivery_charge_type = "NOT_FREE"
        delivery_charge = shipping_cost
        
    original_price = int(round((calculated_sale_price * 1.25) / 100) * 100)
    
    # 5. [출고 지연 리스크 방어] 배송 방식 & 출고소요일
    if use_make_order_delay:
        delivery_method = "MAKE_ORDER"
        outbound_days = 14
    else:
        delivery_method = "AGENT_BUY"
        outbound_days = 7
        
    # 6. [옵션 표준화] 색상 명칭 쿠팡 표준화
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
                "maximumBuyCount": 716,
                "attributes": [
                    {"attributeTypeName": "색상", "attributeValueName": c},
                    {"attributeTypeName": "사이즈", "attributeValueName": s}
                ]
            })
            
    # 7. 100% 실측 고시정보 (상세페이지 참조 0건)
    notices = get_coupang_genuine_notices()
    
    payload = {
        "displayCategoryCode": cat_meta["displayCategoryCode"],
        "sellerProductName": seller_product_name,
        "displayProductName": display_product_name,
        "generalProductName": main_keyword,
        "brand": brand if brand else "자체제작",
        "manufacture": "신지시 슝방 방직품 유한공사",
        "modelName": f"{brand} {main_keyword}".strip(),
        "salePrice": calculated_sale_price,
        "originalPrice": original_price,
        "stockQuantity": 2149,
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
            "representative": "https://cbu01.alicdn.com/img/ibank/O1CN01vslV531UyRJlrPfLq_!!2217475422586-0-cib.jpg",
            "details": [
                "https://cbu01.alicdn.com/img/ibank/O1CN01sD5thV1UyRJmCg9sy_!!2217475422586-0-cib.jpg",
                "https://cbu01.alicdn.com/img/ibank/O1CN01pJ8pHQ1UyRJlWRTv6_!!2217475422586-0-cib.jpg",
                "https://cbu01.alicdn.com/img/ibank/O1CN01XzLoOL1UyRJl0FMKA_!!2217475422586-0-cib.jpg"
            ]
        },
        "notices": notices,
        "attributes": [
            {"attributeTypeName": "사용대상", "attributeValueName": "남녀공용"},
            {"attributeTypeName": "계절", "attributeValueName": "겨울"},
            {"attributeTypeName": "장갑 형태", "attributeValueName": "손가락장갑"},
            {"attributeTypeName": "주요기능", "attributeValueName": "방한/방풍"},
            {"attributeTypeName": "스마트폰 터치 가능여부", "attributeValueName": "터치가능"},
            {"attributeTypeName": "방수여부", "attributeValueName": "생활방수 (방풍/발수 외피)"},
            {"attributeTypeName": "안감재질", "attributeValueName": "극세사 벨벳 기모"}
        ],
        "contents": "<div style='max-width:860px; margin:0 auto;'><p>G-SPORT 프리미엄 겨울 방한 방풍 기모 자전거장갑</p></div>",
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
    p = build_coupang_complete_payload({"mainKeyword": "자전거장갑", "brand": "G-SPORT"})
    print("태그 20개 확인:")
    for i, t in enumerate(p["searchTags"], 1):
        print(f"{i}. {t}")
