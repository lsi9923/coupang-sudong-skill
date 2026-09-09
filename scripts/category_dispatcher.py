#!/usr/bin/env python3
"""
쿠팡/네이버 5대 핵심 카테고리 동적 디스패처 (Multi-Category Dispatcher)
상품의 품목과 카테고리에 따라 100% 달라지는:
1. 법정 고시 상품군 및 세부 항목 (Notices)
2. 검색필터 속성 (Attributes) 및 단위
3. 필수 인증 유형 (Certifications: KC인증, 식약처 수입신고, 안전기준준수)
4. 옵션 축(Axis) 및 가격/배송 규격
을 동적으로 정밀 분기하여 채운다.
"""

CATEGORY_DISPATCHER_REGISTRY = {
    # 1. 패션잡화
    "패션잡화": {
        "keywords": ["장갑", "방한장갑", "자전거장갑", "모자", "벨트", "양말", "머플러", "넥워머", "스카프"],
        "naver": {
            "categoryId": "50001476",
            "categoryName": "스포츠/레저 > 자전거 > 자전거의류/잡화 > 장갑",
            "noticeType": "WEAR",
            "noticeTypeName": "패션잡화 (모자/벨트/액세서리/가방/장갑)",
            "requiredNotices": ["품명 및 모델명", "종류", "소재", "색상", "치수", "제조자/수입자", "제조국", "취급시 주의사항", "품질보증기준", "A/S 책임자와 전화번호"],
            "kcType": "NOT_TARGET",
            "kcDescription": "안전기준준수 품목 (인증대상 아님)"
        },
        "coupang": {
            "displayCategoryCode": 58974,
            "categoryName": "스포츠/레저 > 자전거 > 자전거의류/잡화 > 장갑",
            "noticeCategoryName": "패션잡화 (모자/벨트/액세서리)",
            "requiredNotices": ["품명 및 모델명", "종류", "소재", "치수", "제조자/수입자", "제조국", "취급시 주의사항", "품질보증기준", "A/S 책임자와 전화번호"],
            "mandatoryAttributes": ["사용대상", "계절", "장갑 형태", "주요기능", "스마트폰 터치 가능여부"],
            "certificationType": "NOT_TARGET"
        }
    },
    
    # 2. 소형가전 / 전자기기
    "소형가전": {
        "keywords": ["이어폰", "블루투스", "선풍기", "미니선풍기", "보조배터리", "가습기", "충전기", "헤드셋", "스피커"],
        "naver": {
            "categoryId": "50001597",
            "categoryName": "디지털/가전 > 음향가전 > 블루투스셋 > 블루투스이어폰",
            "noticeType": "DIGITAL",
            "noticeTypeName": "소형전자제품 (소형가전/음향/디지털)",
            "requiredNotices": ["품명 및 모델명", "KC 인증정보", "정격전압, 소비전력", "에너지소비효율등급", "동일모델의 출시년월", "제조자/수입자", "제조국", "크기, 무게", "주요사양", "품질보증기준", "A/S 책임자와 전화번호"],
            "kcType": "TARGET",
            "kcDescription": "방송통신기자재등의 적합등록 (KC R-R-xxx) 또는 안전확인대상"
        },
        "coupang": {
            "displayCategoryCode": 77892,
            "categoryName": "가전디지털 > 음향가전 > 이어폰/헤드폰 > 무선이어폰",
            "noticeCategoryName": "소형전자제품 (음향기기/소형가전)",
            "requiredNotices": ["품명 및 모델명", "KC 인증 필 유무", "정격전압/소비전력", "에너지소비효율등급", "동일모델 출시년월", "제조자/수입자", "제조국", "크기/무게", "주요사양", "품질보증기준", "A/S 책임자와 전화번호"],
            "mandatoryAttributes": ["무선연결방식", "충전단자", "블루투스 버전", "배터리용량", "노이즈캔슬링 여부"],
            "certificationType": "TARGET"
        }
    },
    
    # 3. 주방용품 / 식기류
    "주방용품": {
        "keywords": ["텀블러", "보온병", "물병", "식기", "냄비", "프라이팬", "수저", "밀폐용기", "조리도구"],
        "naver": {
            "categoryId": "50000155",
            "categoryName": "주방용품 > 잔/컵/보온병 > 텀블러/보온병",
            "noticeType": "KITCHEN",
            "noticeTypeName": "주방용품",
            "requiredNotices": ["품명 및 모델명", "재질", "구성품", "크기/용량", "동일모델의 출시년월", "제조자/수입자", "제조국", "수입식품안전관리특별법에 따른 수입신고 확인", "품질보증기준", "A/S 책임자와 전화번호"],
            "kcType": "FOOD_SAFETY",
            "kcDescription": "수입식품안전관리특별법에 따른 수입식품등 검사필 (식품위생검사)"
        },
        "coupang": {
            "displayCategoryCode": 71822,
            "categoryName": "주방용품 > 잔/컵/보온병 > 텀블러/보온병",
            "noticeCategoryName": "주방용품",
            "requiredNotices": ["품명 및 모델명", "재질", "구성품", "크기/용량", "동일모델 출시년월", "제조자/수입자", "제조국", "수입식품안전관리특별법에 따른 수입신고 확인", "품질보증기준", "A/S 책임자와 전화번호"],
            "mandatoryAttributes": ["용량", "보온/보냉 여부", "손잡이 유무", "빨대 포함여부", "식기세척기 사용가능여부"],
            "certificationType": "EXEMPT"
        }
    },
    
    # 4. 패션의류
    "패션의류": {
        "keywords": ["후드티", "맨투맨", "팬츠", "바지", "티셔츠", "자켓", "패딩", "조거팬츠", "원피스"],
        "naver": {
            "categoryId": "50000803",
            "categoryName": "패션의류 > 남성의류 > 티셔츠",
            "noticeType": "CLOTHES",
            "noticeTypeName": "의류",
            "requiredNotices": ["제품 소재", "색상", "치수", "제조자/수입자", "제조국", "세탁방법 및 취급시 주의사항", "제조연월", "품질보증기준", "A/S 책임자와 전화번호"],
            "kcType": "NOT_TARGET",
            "kcDescription": "안전기준준수 품목"
        },
        "coupang": {
            "displayCategoryCode": 56123,
            "categoryName": "패션의류 > 남성의류 > 상의 > 티셔츠/후드",
            "noticeCategoryName": "의류",
            "requiredNotices": ["제품 소재", "색상", "치수", "제조자/수입자", "제조국", "세탁방법 및 취급시 주의사항", "제조연월", "품질보증기준", "A/S 책임자와 전화번호"],
            "mandatoryAttributes": ["상의 사이즈", "핏", "기장", "소재", "계절"],
            "certificationType": "NOT_TARGET"
        }
    },
    
    # 5. 가구 / 캠핑
    "가구캠핑": {
        "keywords": ["체어", "캠핑의자", "테이블", "캠핑테이블", "선반", "수납장", "텐트", "침대", "소파"],
        "naver": {
            "categoryId": "50001402",
            "categoryName": "스포츠/레저 > 캠핑 > 캠핑가구 > 캠핑의자",
            "noticeType": "FURNITURE",
            "noticeTypeName": "가구 (침대/소파/테이블/체어)",
            "requiredNotices": ["품명 및 모델명", "KC 인증정보", "색상", "구성품", "주요 소재", "크기/중량", "제조자/수입자", "제조국", "배송/설치비용", "품질보증기준", "A/S 책임자와 전화번호"],
            "kcType": "NOT_TARGET",
            "kcDescription": "안전기준준수 품목"
        },
        "coupang": {
            "displayCategoryCode": 61240,
            "categoryName": "스포츠/레저 > 캠핑 > 캠핑가구 > 캠핑의자",
            "noticeCategoryName": "가구",
            "requiredNotices": ["품명 및 모델명", "색상", "구성품", "주요 소재", "크기/중량", "제조자/수입자", "제조국", "배송/설치비용", "품질보증기준", "A/S 책임자와 전화번호"],
            "mandatoryAttributes": ["종류", "프레임재질", "내하중", "접이식 여부", "중량"],
            "certificationType": "NOT_TARGET"
        }
    }
}

def resolve_category(keyword: str) -> dict:
    for cat_name, cat_data in CATEGORY_DISPATCHER_REGISTRY.items():
        for kw in cat_data["keywords"]:
            if kw in keyword:
                return {"matchedCategory": cat_name, **cat_data}
    return {"matchedCategory": "패션잡화", **CATEGORY_DISPATCHER_REGISTRY["패션잡화"]}

if __name__ == "__main__":
    import json
    for test_kw in ["자전거장갑", "무선 블루투스 이어폰", "스테인리스 텀블러", "오버핏 기모 후드티", "캠핑 폴딩 체어"]:
        res = resolve_category(test_kw)
        print(f"\n==================== [{test_kw}] ====================")
        print(f"매칭 카테고리군: {res['matchedCategory']}")
        print(f"네이버 고시군: {res['naver']['noticeTypeName']} (항목수: {len(res['naver']['requiredNotices'])}개)")
        print(f"쿠팡 고시군: {res['coupang']['noticeCategoryName']} (항목수: {len(res['coupang']['requiredNotices'])}개)")
        print(f"쿠팡 필수속성: {res['coupang']['mandatoryAttributes']}")
        print(f"인증요건: 네이버({res['naver']['kcType']}) / 쿠팡({res['coupang']['certificationType']})")
