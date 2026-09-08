#!/usr/bin/env python3
"""
쿠팡/네이버 상품정보제공고시 100% 실측 데이터 전수 매퍼 (상세페이지 참조 0건 원칙)
1688 공장(신지시 슝방 방직품 유한공사) 원천 스펙 전수 반영:
- 총장 23cm, 손바닥폭 10cm, 중량 85g, 부피 184cm³
- 겉감 폴리에스테르 95% + 스판덱스 5% / 안감 극세사 벨벳기모 100% / 손바닥 논슬립 실리콘 / 엄지·검지 터치원단
- 30℃ 이하 미온수 중성세제 손세탁, 표백제/건조기 금지
"""

# 공장 및 원천 실측 데이터 상수
GENUINE_PRODUCT_SPEC = {
    "productNameModel": "G-SPORT 방한 라이딩 장갑 (G-01)",
    "coupangModelName": "G-SPORT 자전거장갑",
    "productType": "방한 방풍 자전거 라이딩 장갑 (손가락장갑)",
    "material": "겉감: 고밀도 방풍 폴리에스테르 95%, 스판덱스 5% / 안감: 극세사 보온 벨벳 기모 100% / 손바닥: 논슬립 허니컴 실리콘 / 손가락: 전도성 터치 패널",
    "dimensions": "총장 23cm, 손바닥 폭 10cm, 권장 손둘레 19~23cm 대응 (남녀공용 프리사이즈), 실측 중량 85g(한 켤레, 포장부피 184cm³)",
    "colors": "블랙, 블랙 그레이(투톤), 멜란지 그레이 (총 3컬러)",
    "manufacturer": "신지시 슝방 방직품 유한공사 (Xinji Xiongfang Textile Co., Ltd.)",
    "importer": "판매자 협력사 수입 / 해외직구",
    "origin": "중국 (China, 허베이성 신지시 생산 / 스자좡 발송)",
    "washCare": "30℃ 이하 미온수 중성세제 단독 손세탁 권장, 표백제 및 열풍 건조기 사용 금지, 비틀어 짜지 말고 그늘 자연건조, 다림질 금지",
    "warranty": "전자상거래 등에서의 소비자보호에 관한 법률 및 공정거래위원회 고시 소비자분쟁해결기준에 의거 보상 (수령 후 7일 이내 초기 불량 시 100% 무상 교환/반품)",
    "asContact": "판매자 고객센터 (네이버 톡톡 및 고객센터 1:1 문의창구)"
}

def get_naver_genuine_notices() -> list[dict]:
    s = GENUINE_PRODUCT_SPEC
    return [
        {"name": "품명 및 모델명", "value": s["productNameModel"]},
        {"name": "종류", "value": s["productType"]},
        {"name": "소재", "value": s["material"]},
        {"name": "색상", "value": s["colors"]},
        {"name": "치수", "value": s["dimensions"]},
        {"name": "제조자/수입자", "value": f"{s['manufacturer']} / {s['importer']}"},
        {"name": "제조국", "value": s["origin"]},
        {"name": "취급시 주의사항", "value": s["washCare"]},
        {"name": "품질보증기준", "value": s["warranty"]},
        {"name": "A/S 책임자와 전화번호", "value": s["asContact"]}
    ]

def get_coupang_genuine_notices() -> list[dict]:
    s = GENUINE_PRODUCT_SPEC
    cat = "패션잡화 (모자/벨트/액세서리)"
    return [
        {"noticeCategoryName": cat, "noticeCategoryDetailName": "품명 및 모델명", "content": s["coupangModelName"]},
        {"noticeCategoryName": cat, "noticeCategoryDetailName": "종류", "content": s["productType"]},
        {"noticeCategoryName": cat, "noticeCategoryDetailName": "소재", "content": s["material"]},
        {"noticeCategoryName": cat, "noticeCategoryDetailName": "치수", "content": s["dimensions"]},
        {"noticeCategoryName": cat, "noticeCategoryDetailName": "제조자/수입자", "content": f"{s['manufacturer']} / {s['importer']}"},
        {"noticeCategoryName": cat, "noticeCategoryDetailName": "제조국", "content": s["origin"]},
        {"noticeCategoryName": cat, "noticeCategoryDetailName": "취급시 주의사항", "content": s["washCare"]},
        {"noticeCategoryName": cat, "noticeCategoryDetailName": "품질보증기준", "content": s["warranty"]},
        {"noticeCategoryName": cat, "noticeCategoryDetailName": "A/S 책임자와 전화번호", "content": s["asContact"]}
    ]

if __name__ == "__main__":
    import json
    print("=== 네이버 고시 전수 실측값 ===")
    print(json.dumps(get_naver_genuine_notices(), ensure_ascii=False, indent=2))
    print("=== 쿠팡 고시 전수 실측값 ===")
    print(json.dumps(get_coupang_genuine_notices(), ensure_ascii=False, indent=2))
