#!/usr/bin/env python3
"""
쿠팡/네이버 10대 대표 카테고리 동적 디스패처 (우선순위 및 구체성 매칭 최적화)
"""

# 우선순위: 반려동물, 차량용품, 소형가전 등 구체적 카테고리가 일반(주방, 패션)보다 먼저 평가됨
CATEGORY_10_REGISTRY = {
    # 1. 반려동물용품 (식기, 장난감 등 중복 단어 우선 판별)
    "반려동물": {
        "keywords": ["강아지식기", "노즈워크", "급식기", "사료그릇", "고양이장난감", "하네스", "배변패드", "반려동물", "강아지", "고양이", "애견", "애묘"],
        "naver": {
            "categoryId": "50001648",
            "categoryName": "생활/건강 > 반려동물 > 강아지 식기/급수기 > 식기/식탁",
            "noticeType": "PET",
            "noticeTypeName": "반려동물용품",
            "requiredNotices": ["품명 및 모델명", "재질", "크기/중량", "색상", "제조자/수입자", "제조국", "취급방법 및 취급시 주의사항", "품질보증기준", "A/S 책임자와 전화번호"],
            "kcType": "NOT_TARGET"
        },
        "coupang": {
            "displayCategoryCode": 74512,
            "categoryName": "반려동물용품 > 강아지 식기/급수기 > 식기/급식기",
            "noticeCategoryName": "반려동물용품",
            "requiredNotices": ["품명 및 모델명", "재질", "크기/중량", "색상", "제조자/수입자", "제조국", "취급방법 및 주의사항", "품질보증기준", "A/S 책임자와 전화번호"],
            "mandatoryAttributes": ["반려동물 크기", "식기 종류", "용량", "미끄럼방지 유무", "소재"],
            "certificationType": "NOT_TARGET"
        }
    },

    # 2. 차량용품
    "차량용품": {
        "keywords": ["차량용거치대", "맥세이프거치대", "차량용충전기", "차량용", "맥세이프", "트렁크매트", "시트커버", "송풍구거치대"],
        "naver": {
            "categoryId": "50001053",
            "categoryName": "디지털/가전 > 휴대폰액세서리 > 거치대 > 차량용거치대",
            "noticeType": "CAR",
            "noticeTypeName": "자동차용품 (네비게이션/블랙박스/액세서리)",
            "requiredNotices": ["품명 및 모델명", "KC 인증 필 유무", "정격전압, 소비전력", "동일모델의 출시년월", "제조자/수입자", "제조국", "크기, 무게", "주요사양", "품질보증기준", "A/S 책임자와 전화번호"],
            "kcType": "TARGET"
        },
        "coupang": {
            "displayCategoryCode": 63980,
            "categoryName": "자동차용품 > 인테리어소품 > 휴대폰거치대 > 무선충전거치대",
            "noticeCategoryName": "자동차용품",
            "requiredNotices": ["품명 및 모델명", "KC 인증 필 유무", "정격전압/소비전력", "동일모델 출시년월", "제조자/수입자", "제조국", "크기/무게", "주요사양", "품질보증기준", "A/S 책임자와 전화번호"],
            "mandatoryAttributes": ["고정방식", "충전방식", "최대출력", "맥세이프 호환여부", "회전 여부"],
            "certificationType": "TARGET"
        }
    },

    # 3. 소형가전 / 음향기기
    "소형가전": {
        "keywords": ["이어폰", "블루투스", "무선이어폰", "선풍기", "미니선풍기", "보조배터리", "가습기", "헤드셋", "스피커", "충전기"],
        "naver": {
            "categoryId": "50001597",
            "categoryName": "디지털/가전 > 음향가전 > 블루투스셋 > 블루투스이어폰",
            "noticeType": "DIGITAL",
            "noticeTypeName": "소형전자제품 (소형가전/음향/디지털)",
            "requiredNotices": ["품명 및 모델명", "KC 인증정보", "정격전압, 소비전력", "에너지소비효율등급", "동일모델의 출시년월", "제조자/수입자", "제조국", "크기, 무게", "주요사양", "품질보증기준", "A/S 책임자와 전화번호"],
            "kcType": "TARGET"
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

    # 4. 스포츠 / 헬스용품
    "스포츠헬스": {
        "keywords": ["튜빙밴드", "저항밴드", "요가매트", "폼롤러", "덤벨", "아령", "악력기", "피트니스", "홈트"],
        "naver": {
            "categoryId": "50001428",
            "categoryName": "스포츠/레저 > 헬스/피트니스 > 웨이트기구 > 튜빙/스트레칭밴드",
            "noticeType": "SPORTS",
            "noticeTypeName": "체육용품",
            "requiredNotices": ["품명 및 모델명", "크기, 중량", "색상", "재질", "제품구성", "동일모델의 출시년월", "제조자/수입자", "제조국", "상품별 세부사양", "품질보증기준", "A/S 책임자와 전화번호"],
            "kcType": "NOT_TARGET"
        },
        "coupang": {
            "displayCategoryCode": 59120,
            "categoryName": "스포츠/레저 > 헬스/피트니스 > 피트니스소품 > 밴드/스트랩",
            "noticeCategoryName": "체육용품",
            "requiredNotices": ["품명 및 모델명", "크기/중량", "색상", "재질", "제품구성", "동일모델 출시년월", "제조자/수입자", "제조국", "상품별 세부사양", "품질보증기준", "A/S 책임자와 전화번호"],
            "mandatoryAttributes": ["강도", "재질", "제품구성", "길이", "사용부위"],
            "certificationType": "NOT_TARGET"
        }
    },

    # 5. 가구 / 캠핑
    "가구캠핑": {
        "keywords": ["캠핑체어", "캠핑의자", "캠핑테이블", "릴렉스체어", "접이식의자", "텐트", "수납장"],
        "naver": {
            "categoryId": "50001402",
            "categoryName": "스포츠/레저 > 캠핑 > 캠핑가구 > 캠핑의자",
            "noticeType": "FURNITURE",
            "noticeTypeName": "가구 (침대/소파/테이블/체어)",
            "requiredNotices": ["품명 및 모델명", "KC 인증정보", "색상", "구성품", "주요 소재", "크기/중량", "제조자/수입자", "제조국", "배송/설치비용", "품질보증기준", "A/S 책임자와 전화번호"],
            "kcType": "NOT_TARGET"
        },
        "coupang": {
            "displayCategoryCode": 61240,
            "categoryName": "스포츠/레저 > 캠핑 > 캠핑가구 > 캠핑의자",
            "noticeCategoryName": "가구",
            "requiredNotices": ["품명 및 모델명", "색상", "구성품", "주요 소재", "크기/중량", "제조자/수입자", "제조국", "배송/설치비용", "품질보증기준", "A/S 책임자와 전화번호"],
            "mandatoryAttributes": ["종류", "프레임재질", "내하중", "접이식 여부", "중량"],
            "certificationType": "NOT_TARGET"
        }
    },

    # 6. 화장품 / 뷰티
    "화장품": {
        "keywords": ["수분크림", "에센스", "세럼", "로션", "앰플", "립스틱", "클렌저", "선크림", "스킨케어", "크림"],
        "naver": {
            "categoryId": "50000190",
            "categoryName": "화장품/미용 > 스킨케어 > 크림",
            "noticeType": "COSMETIC",
            "noticeTypeName": "화장품",
            "requiredNotices": ["내용물의 용량 또는 중량", "제품 주요 사양", "사용기한 또는 개봉 후 사용기간", "사용방법", "화장품제조업자 및 화장품책임판매업자", "제조국", "화장품법에 따라 기재·표시하여야 하는 모든 성분", "기능성 화장품 심사 필 유무", "사용할 때의 주의사항", "품질보증기준", "A/S 책임자와 전화번호"],
            "kcType": "COSMETIC_REG"
        },
        "coupang": {
            "displayCategoryCode": 67890,
            "categoryName": "뷰티 > 스킨케어 > 크림/올인원 > 수분크림",
            "noticeCategoryName": "화장품",
            "requiredNotices": ["용량 또는 중량", "제품 주요 사양", "사용기한 또는 개봉 후 사용기간", "사용방법", "제조업자 및 책임판매업자", "제조국", "모든 성분", "기능성 화장품 여부", "사용 시의 주의사항", "품질보증기준", "소비자상담관련 전화번호"],
            "mandatoryAttributes": ["피부타입", "피부고민", "용량", "주요제품특징", "사용부위"],
            "certificationType": "NOT_TARGET"
        }
    },

    # 7. 생활 / 욕실용품
    "생활욕실": {
        "keywords": ["샤워헤드", "필터샤워기", "샤워기", "수전", "배수구", "칫솔살균기", "욕실"],
        "naver": {
            "categoryId": "50001099",
            "categoryName": "생활/건강 > 욕실용품 > 샤워기/수전용품 > 샤워기헤드",
            "noticeType": "BATH",
            "noticeTypeName": "생활위생용품",
            "requiredNotices": ["품명 및 모델명", "크기, 중량", "색상", "재질", "제품구성", "동일모델의 출시년월", "제조자/수입자", "제조국", "품질보증기준", "A/S 책임자와 전화번호"],
            "kcType": "NOT_TARGET"
        },
        "coupang": {
            "displayCategoryCode": 81245,
            "categoryName": "생활용품 > 욕실용품 > 샤워기/호스 > 샤워헤드",
            "noticeCategoryName": "생활위생용품",
            "requiredNotices": ["품명 및 모델명", "크기/중량", "색상", "재질", "제품구성", "동일모델 출시년월", "제조자/수입자", "제조국", "품질보증기준", "A/S 책임자와 전화번호"],
            "mandatoryAttributes": ["샤워헤드 기능", "절수 기능 유무", "필터 포함 여부", "헤드 직경", "연결 규격"],
            "certificationType": "NOT_TARGET"
        }
    },

    # 8. 주방용품 / 식기
    "주방용품": {
        "keywords": ["텀블러", "보온병", "물병", "냄비", "프라이팬", "수저", "밀폐용기", "조리도구", "컵", "주방식기", "식기세척기용"],
        "naver": {
            "categoryId": "50000155",
            "categoryName": "주방용품 > 잔/컵/보온병 > 텀블러/보온병",
            "noticeType": "KITCHEN",
            "noticeTypeName": "주방용품",
            "requiredNotices": ["품명 및 모델명", "재질", "구성품", "크기/용량", "동일모델의 출시년월", "제조자/수입자", "제조국", "수입식품안전관리특별법에 따른 수입신고 확인", "품질보증기준", "A/S 책임자와 전화번호"],
            "kcType": "FOOD_SAFETY"
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

    # 9. 패션의류
    "패션의류": {
        "keywords": ["후드티", "맨투맨", "팬츠", "바지", "티셔츠", "자켓", "패딩", "조거팬츠", "원피스", "청바지"],
        "naver": {
            "categoryId": "50000803",
            "categoryName": "패션의류 > 남성의류 > 티셔츠",
            "noticeType": "CLOTHES",
            "noticeTypeName": "의류",
            "requiredNotices": ["제품 소재", "색상", "치수", "제조자/수입자", "제조국", "세탁방법 및 취급시 주의사항", "제조연월", "품질보증기준", "A/S 책임자와 전화번호"],
            "kcType": "NOT_TARGET"
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

    # 10. 패션잡화 (기본)
    "패션잡화": {
        "keywords": ["장갑", "방한장갑", "자전거장갑", "라이딩장갑", "모자", "벨트", "양말", "머플러", "넥워머", "스카프", "잡화"],
        "naver": {
            "categoryId": "50001476",
            "categoryName": "스포츠/레저 > 자전거 > 자전거의류/잡화 > 장갑",
            "noticeType": "WEAR",
            "noticeTypeName": "패션잡화 (모자/벨트/액세서리/가방/장갑)",
            "requiredNotices": ["품명 및 모델명", "종류", "소재", "색상", "치수", "제조자/수입자", "제조국", "취급시 주의사항", "품질보증기준", "A/S 책임자와 전화번호"],
            "kcType": "NOT_TARGET"
        },
        "coupang": {
            "displayCategoryCode": 58974,
            "categoryName": "스포츠/레저 > 자전거 > 자전거의류/잡화 > 장갑",
            "noticeCategoryName": "패션잡화 (모자/벨트/액세서리)",
            "requiredNotices": ["품명 및 모델명", "종류", "소재", "치수", "제조자/수입자", "제조국", "취급시 주의사항", "품질보증기준", "A/S 책임자와 전화번호"],
            "mandatoryAttributes": ["사용대상", "계절", "장갑 형태", "주요기능", "스마트폰 터치 가능여부"],
            "certificationType": "NOT_TARGET"
        }
    }
}

def resolve_10_category(keyword: str) -> dict:
    target_clean = keyword.replace(" ", "")
    for cat_name, cat_data in CATEGORY_10_REGISTRY.items():
        for kw in cat_data["keywords"]:
            if kw in keyword or kw in target_clean:
                return {"matchedCategory": cat_name, **cat_data}
    return {"matchedCategory": "패션잡화", **CATEGORY_10_REGISTRY["패션잡화"]}
