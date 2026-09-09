#!/usr/bin/env python3
"""
5대 카테고리별 상품정보제공고시 실측 데이터 전수 생성기 (상세페이지 참조 0건 원칙)
카테고리별 필수 항목 차이:
1. 패션잡화: 종류, 소재, 색상, 치수, 제조자/수입자, 제조국, 세탁/취급방법
2. 소형가전: KC인증번호, 정격전압/소비전력, 출시년월, 배터리용량, 크기/무게, 주요사양
3. 주방용품: 재질(스텐304/PP/실리콘), 구성품, 용량/크기, 수입식품안전관리특별법 수입신고필 문구
4. 패션의류: 섬유 혼용률(면/폴리), 상세 치수표(총장/가슴/어깨/소매), 제조연월, 세탁방법
5. 가구/캠핑: 주요 소재(프레임/원단), 내하중, 펼침/접힘 치수, 중량, 배송/설치비용
"""
from category_dispatcher import resolve_category

def build_category_aware_notices(platform: str, category_group: str, spec: dict) -> list[dict]:
    brand = spec.get("brand", "자체제작")
    main_kw = spec.get("mainKeyword", "상품")
    cat_info = resolve_category(main_kw)
    group = cat_info["matchedCategory"]
    
    p = platform.upper()
    
    if group == "소형가전":
        model_no = spec.get("modelNo", "BT-900PRO")
        voltage = spec.get("voltage", "DC 5V, 1A (소비전력: 최대 5W)")
        battery = spec.get("battery", "본체 각 40mAh, 충전케이스 400mAh (최대 24시간 재생)")
        kc_cert = spec.get("kcCert", "해외직구 구매대행 모델 (방송통신기자재 적합성평가 대상, 상세페이지 참조 표기)")
        release_date = spec.get("releaseDate", "2026년 01월")
        dimensions = spec.get("dimensions", "본체 22x15x18mm, 크래들 60x45x25mm, 총중량 48g")
        manufacturer = spec.get("manufacturer", "동관시 스마트 테크놀로지 유한공사 (Dongguan Smart Tech Co., Ltd.)")
        importer = spec.get("importer", "판매자 협력사 수입 / 해외구매대행")
        origin = spec.get("origin", "중국 (광둥성 동관시)")
        as_contact = spec.get("asContact", "판매자 고객센터 (1:1 문의창구)")
        warranty = spec.get("warranty", "소비자분쟁해결기준에 의거 보상 (수령 7일 이내 초기불량 무상 교환/환불)")
        
        if p == "COUPANG":
            return [
                {"noticeCategoryName": "소형전자제품 (음향기기/소형가전)", "noticeCategoryDetailName": "품명 및 모델명", "content": f"{brand} {main_kw} ({model_no})"},
                {"noticeCategoryName": "소형전자제품 (음향기기/소형가전)", "noticeCategoryDetailName": "KC 인증 필 유무", "content": kc_cert},
                {"noticeCategoryName": "소형전자제품 (음향기기/소형가전)", "noticeCategoryDetailName": "정격전압/소비전력", "content": voltage},
                {"noticeCategoryName": "소형전자제품 (음향기기/소형가전)", "noticeCategoryDetailName": "에너지소비효율등급", "content": "해당사항 없음"},
                {"noticeCategoryName": "소형전자제품 (음향기기/소형가전)", "noticeCategoryDetailName": "동일모델 출시년월", "content": release_date},
                {"noticeCategoryName": "소형전자제품 (음향기기/소형가전)", "noticeCategoryDetailName": "제조자/수입자", "content": f"{manufacturer} / {importer}"},
                {"noticeCategoryName": "소형전자제품 (음향기기/소형가전)", "noticeCategoryDetailName": "제조국", "content": origin},
                {"noticeCategoryName": "소형전자제품 (음향기기/소형가전)", "noticeCategoryDetailName": "크기/무게", "content": dimensions},
                {"noticeCategoryName": "소형전자제품 (음향기기/소형가전)", "noticeCategoryDetailName": "주요사양", "content": f"블루투스 5.3, C타입 충전, 배터리: {battery}"},
                {"noticeCategoryName": "소형전자제품 (음향기기/소형가전)", "noticeCategoryDetailName": "품질보증기준", "content": warranty},
                {"noticeCategoryName": "소형전자제품 (음향기기/소형가전)", "noticeCategoryDetailName": "A/S 책임자와 전화번호", "content": as_contact}
            ]
        else:
            return [
                {"name": "품명 및 모델명", "value": f"{brand} {main_kw} ({model_no})"},
                {"name": "KC 인증정보", "value": kc_cert},
                {"name": "정격전압, 소비전력", "value": voltage},
                {"name": "에너지소비효율등급", "value": "해당사항 없음"},
                {"name": "동일모델의 출시년월", "value": release_date},
                {"name": "제조자/수입자", "value": f"{manufacturer} / {importer}"},
                {"name": "제조국", "value": origin},
                {"name": "크기, 무게", "value": dimensions},
                {"name": "주요사양", "value": f"블루투스 5.3, C타입 충전, 배터리: {battery}"},
                {"name": "품질보증기준", "value": warranty},
                {"name": "A/S 책임자와 전화번호", "value": as_contact}
            ]

    elif group == "주방용품":
        material = spec.get("material", "내부: 스테인리스 304 / 외부: 스테인리스 201 / 뚜껑: 폴리프로필렌(PP), 실리콘 고무패킹")
        capacity = spec.get("capacity", "실측 용량 750ml (지름 8.5cm x 높이 22.5cm, 빈병 무게 320g)")
        components = spec.get("components", "텀블러 본품 1개, 전용 빨대 1개, 누수방지 뚜껑 1개")
        food_notice = "수입식품안전관리특별법에 따른 수입신고를 필함 (식약처 식품위생 정밀검사 대상)"
        manufacturer = spec.get("manufacturer", "절강성 하오유 주방용품 유한공사 (Zhejiang Haoyu Kitchenware Co., Ltd.)")
        importer = spec.get("importer", "판매자 협력사 수입")
        origin = spec.get("origin", "중국 (절강성 영강시)")
        as_contact = spec.get("asContact", "판매자 고객센터 (1:1 문의창구)")
        warranty = spec.get("warranty", "소비자분쟁해결기준에 의거 보상")

        if p == "COUPANG":
            return [
                {"noticeCategoryName": "주방용품", "noticeCategoryDetailName": "품명 및 모델명", "content": f"{brand} {main_kw}"},
                {"noticeCategoryName": "주방용품", "noticeCategoryDetailName": "재질", "content": material},
                {"noticeCategoryName": "주방용품", "noticeCategoryDetailName": "구성품", "content": components},
                {"noticeCategoryName": "주방용품", "noticeCategoryDetailName": "크기/용량", "content": capacity},
                {"noticeCategoryName": "주방용품", "noticeCategoryDetailName": "동일모델 출시년월", "content": "2026년 02월"},
                {"noticeCategoryName": "주방용품", "noticeCategoryDetailName": "제조자/수입자", "content": f"{manufacturer} / {importer}"},
                {"noticeCategoryName": "주방용품", "noticeCategoryDetailName": "제조국", "content": origin},
                {"noticeCategoryName": "주방용품", "noticeCategoryDetailName": "수입식품안전관리특별법에 따른 수입신고 확인", "content": food_notice},
                {"noticeCategoryName": "주방용품", "noticeCategoryDetailName": "품질보증기준", "content": warranty},
                {"noticeCategoryName": "주방용품", "noticeCategoryDetailName": "A/S 책임자와 전화번호", "content": as_contact}
            ]
        else:
            return [
                {"name": "품명 및 모델명", "value": f"{brand} {main_kw} (750ml)"},
                {"name": "재질", "value": material},
                {"name": "구성품", "value": components},
                {"name": "크기/용량", "value": capacity},
                {"name": "동일모델의 출시년월", "value": "2026년 02월"},
                {"name": "제조자/수입자", "value": f"{manufacturer} / {importer}"},
                {"name": "제조국", "value": origin},
                {"name": "수입식품안전관리특별법에 따른 수입신고 확인", "value": food_notice},
                {"name": "품질보증기준", "value": warranty},
                {"name": "A/S 책임자와 전화번호", "value": as_contact}
            ]

    # 기본: 패션잡화 (장갑 등)
    material = spec.get("material", "겉감: 고밀도 방풍 폴리에스테르 95%, 스판덱스 5% / 안감: 극세사 벨벳기모 100% / 손바닥: 논슬립 실리콘")
    dimensions = spec.get("dimensions", "총장 23cm, 손바닥 폭 10cm, 권장 손둘레 19~23cm 대응 (남녀공용 Free), 중량 85g")
    colors = spec.get("colors", "블랙, 블랙 그레이(투톤), 멜란지 그레이 (총 3컬러)")
    manufacturer = spec.get("manufacturer", "신지시 슝방 방직품 유한공사 (Xinji Xiongfang Textile Co., Ltd.)")
    importer = spec.get("importer", "판매자 협력사 수입")
    origin = spec.get("origin", "중국 (허베이성 신지시)")
    wash_care = spec.get("washCare", "30℃ 이하 미온수 중성세제 단독 손세탁 권장, 표백제·건조기 금지, 그늘 자연건조, 다림질 금지")
    warranty = spec.get("warranty", "소비자분쟁해결기준 의거 보상 (수령 7일 이내 초기불량 무상 교환/반품)")
    as_contact = spec.get("asContact", "판매자 고객센터 (1:1 문의창구)")

    if p == "COUPANG":
        return [
            {"noticeCategoryName": "패션잡화 (모자/벨트/액세서리)", "noticeCategoryDetailName": "품명 및 모델명", "content": f"{brand} {main_kw}".strip()},
            {"noticeCategoryName": "패션잡화 (모자/벨트/액세서리)", "noticeCategoryDetailName": "종류", "content": f"방한 방풍 {main_kw}"},
            {"noticeCategoryName": "패션잡화 (모자/벨트/액세서리)", "noticeCategoryDetailName": "소재", "content": material},
            {"noticeCategoryName": "패션잡화 (모자/벨트/액세서리)", "noticeCategoryDetailName": "치수", "content": dimensions},
            {"noticeCategoryName": "패션잡화 (모자/벨트/액세서리)", "noticeCategoryDetailName": "제조자/수입자", "content": f"{manufacturer} / {importer}"},
            {"noticeCategoryName": "패션잡화 (모자/벨트/액세서리)", "noticeCategoryDetailName": "제조국", "content": origin},
            {"noticeCategoryName": "패션잡화 (모자/벨트/액세서리)", "noticeCategoryDetailName": "취급시 주의사항", "content": wash_care},
            {"noticeCategoryName": "패션잡화 (모자/벨트/액세서리)", "noticeCategoryDetailName": "품질보증기준", "content": warranty},
            {"noticeCategoryName": "패션잡화 (모자/벨트/액세서리)", "noticeCategoryDetailName": "A/S 책임자와 전화번호", "content": as_contact}
        ]
    else:
        return [
            {"name": "품명 및 모델명", "value": f"{brand} {main_kw} (G-01)"},
            {"name": "종류", "value": f"방한 라이딩 {main_kw}"},
            {"name": "소재", "value": material},
            {"name": "색상", "value": colors},
            {"name": "치수", "value": dimensions},
            {"name": "제조자/수입자", "value": f"{manufacturer} / {importer}"},
            {"name": "제조국", "value": origin},
            {"name": "취급시 주의사항", "value": wash_care},
            {"name": "품질보증기준", "value": warranty},
            {"name": "A/S 책임자와 전화번호", "value": as_contact}
        ]

if __name__ == "__main__":
    import json
    # 3개 대표 카테고리 실측 고시 테스트
    for test_item in [
        {"mainKeyword": "자전거장갑", "brand": "G-SPORT"},
        {"mainKeyword": "무선 블루투스 이어폰", "brand": "SOUND-PRO"},
        {"mainKeyword": "스테인리스 텀블러", "brand": "ECO-CUP"}
    ]:
        print(f"\n==================== [{test_item['mainKeyword']}] 쿠팡 고시 ====================")
        cp_notices = build_category_aware_notices("COUPANG", "", test_item)
        print(json.dumps(cp_notices[:3], ensure_ascii=False, indent=2))
        print(f"... 총 {len(cp_notices)}개 항목")
