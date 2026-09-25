# -*- coding: utf-8 -*-
"""
buggy_2.py  ―  카테고리별 매출 집계 (pandas 버전)

dirty_sales.csv를 pandas로 읽어 카테고리별 매출 합계를 구하려 한다.
그런데 실행하자마자 죽는다.

[과제] Traceback을 얻어 예외 타입을 확인하고,
       '원인을 데이터에서 직접 확인'한 뒤(힌트: 실제 컬럼명이 무엇인가?)
       코드를 수정하라.
"""
import pandas as pd

def load(path):
    df = pd.read_csv(path, encoding="utf-8")
    return df

def summarize(df):
    # 단가 x 수량으로 매출액 컬럼을 만든 뒤 카테고리별 합계를 낸다
    # df["매출액"] = df["단가"] * df["수량"]        # <-- 여기가 문제의 줄
    df["매출액"] = df["price"] * df["quantity"]  # FIXED : 실제 컬럼명에 맞게 수정
    return df.groupby("category")["매출액"].sum()

if __name__ == "__main__":
    df = load("dirty_sales.csv")
    result = summarize(df)
    print(result)

    # 회귀 없음 확인 및 정상 데이터 처리 증빙

    print("\n--테스트--")
    # 1) 정상 컬럼명('price', 'quantity')을 가진 가상의 테스트 데이터프레임 생성
    test_data = pd.DataFrame({
        "category": ["과자", "과자", "음료"],
        "price": [1000, 2000, 3000],
        "quantity": [2, 1, 3]
    })
    
    # 2) 수정한 summarize 함수 실행 
    # 기대값: 과자 = (1000*2) + (2000*1) = 4000 / 음료 = (3000*3) = 9000
    test_result = summarize(test_data)
    
    print("1) 테스트 정상 데이터:")
    print(test_data[['category', 'price', 'quantity']])
    print("\n2) 실제 계산된 카테고리별 집계 결과:")
    print(test_result)
    
    # 3) 결과 검증
    is_snack_correct = test_result["과자"] == 4000
    is_drink_correct = test_result["음료"] == 9000
    
    print(f"\n3) 검증(과자 카테고리 기대치 4000과 일치 여부): {is_snack_correct}")
    print(f"4) 검증(음료 카테고리 기대치 9000과 일치 여부): {is_drink_correct}")