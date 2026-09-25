# -*- coding: utf-8 -*-
"""
buggy_1.py  ―  판매 데이터 매출 집계 (csv 모듈 버전)

dirty_sales.csv를 한 줄씩 읽어 '매출액 = 단가 x 수량'을 누적한다.
잘 돌아가는 것처럼 보이지만, 어떤 행에서 갑자기 멈춘다.

[과제] 이 스크립트를 실행해 Traceback을 얻고,
       진단 3단계 루틴(무엇이 / 어디서 / 왜)으로 원인을 특정한 뒤
       전처리로 해결하라. (힌트: 예외 타입은 무엇인가?)
"""
import csv
import os

def calc_total(path):
    total = 0
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)  # 사전타입으로 데이터를 읽음.
        for i, row in enumerate(reader):
            row["price"] = row["price"].replace(",", "")  # FIXED : 콤마를 제거해서 숫자로 변환 가능하게 함
            row["price"] = row["price"].replace("원", "")  # FIXED : '원' 문자를 제거해서 숫자로 변환 가능하게 함
            if not row["price"]:
                continue # FIXED : price 값이 비어있으면 건너뛰도록 함
            price = int(row["price"])        # <-- 여기가 문제의 줄
            qty = int(row["quantity"])
            total += price * qty
    return total

if __name__ == "__main__":
    total = calc_total("./Week4/dirty_sales.csv")
    print(f"총 매출액: {total:,}원")

    # 회귀 없음 확인 및 정상 데이터 처리 증빙
    print("\n--테스트--")
    # 1) 정상 데이터만 존재하는 가상의 테스트 파일 임시 생성
    test_filepath = "test_normal_data.csv"
    with open(test_filepath, "w", encoding="utf-8") as f:
        f.write("date,product,category,price,quantity,stock\n")
        f.write("2026-09-25,상품A,카테고리1,1000,2,10\n")  # 1000 * 2 = 2000
        f.write("2026-09-25,상품B,카테고리2,2000,3,10\n")  # 2000 * 3 = 6000

    # 2) 테스트 파일로 calc_total 실행 (예상 결과: 8000)
    test_total = calc_total(test_filepath)
    expected_total = 8000
    
    print("테스트 정상 데이터: (단가 1000 x 수량 2) + (단가 2000 x 수량 3)")
    print(f"실제 계산된 총 매출액: {test_total}")
    print(f"검증(예상치 8000과 일치 여부): {test_total == expected_total}")
    
    # 3) 테스트가 끝난 후 임시 파일 삭제
    if os.path.exists(test_filepath):
        os.remove(test_filepath)
