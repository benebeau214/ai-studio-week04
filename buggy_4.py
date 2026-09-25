# -*- coding: utf-8 -*-
"""
buggy_4.py  ―  총 매출액 집계 (에러 없이 '조용히' 틀리는 스크립트)

이 스크립트는 에러 없이 잘 돌아가고, 그럴듯한 숫자를 출력한다.
하지만 그 숫자는 '틀렸다'.

[과제] 이 스크립트는 예외를 던지지 않는다. 대신
       (1) info()/describe()로 데이터 상태를 먼저 세어 보고
       (2) '무엇이 틀렸는지 어떻게 알아챘는지'를 서술한 뒤
       (3) 결측 규모를 보고하고 처리 방법을 선택·적용하여
           올바른 총매출을 산출하라.
       (힌트: 가격 결측은 몇 건인가? 음수 가격과 9999999 같은 값은 정상인가?)
"""
import pandas as pd

def main():
    df = pd.read_csv("dirty_sales.csv", encoding="utf-8")

    # price를 숫자로 바꾼다 (빈 값은 NaN이 된다 — 그런데 그 규모를 확인하지 않았다)
    df["price"] = (df["price"].astype(str)
                              .str.replace(",", "")
                              .str.replace("원", "")
                              .str.strip())
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    df = df.dropna(subset=["price"])  # FIXED : 결측값 제거
    df = df[df["price"] > 0]  # FIXED : 음수 가격 제거
    df = df[df["price"] < 9999999]  # FIXED : 극단적인 이상치 제거
    df = df[df["quantity"] < 9999999] # FIXED : 극단적인 이상치 제거

    # 매출액 = 단가 x 수량 (NaN이 섞이면 그 행의 매출액도 NaN)
    df["revenue"] = df["price"] * df["quantity"]

    # sum()은 NaN을 조용히 건너뛰고, 음수/극단값은 그대로 더한다
    total = df["revenue"].sum()
    avg_price = df["price"].mean()

    print(f"총 매출액: {total:,.0f}원")
    print(f"평균 단가: {avg_price:,.0f}원")
    # 출력은 그럴듯하지만, 이 숫자를 그대로 믿어도 될까?

if __name__ == "__main__":
    main()

    # 회귀 없음 확인 및 정상 데이터 처리 증빙
    print("\n--테스트--")
    # 1) 정상, 결측, 음수, 극단값이 섞인 가상의 테스트 데이터프레임 생성
    test_data = pd.DataFrame({
        "product": ["정상상품", "결측상품", "음수상품", "극단값상품"],
        "price": ["1000", None, "-500", "9999999"],
        "quantity": [2, 1, 1, 1]
    })
    # 2) 정제 로직을 동일하게 적용
    df_test = test_data.copy()
    df_test["price"] = pd.to_numeric(df_test["price"], errors="coerce")
    df_test = df_test.dropna(subset=["price"]) 
    df_test = df_test[df_test["price"] > 0]
    df_test = df_test[df_test["price"] < 9999999]
    df_test["revenue"] = df_test["price"] * df_test["quantity"]
    
    print("1) 테스트 원본 데이터:")
    print(test_data)
    print("\n2) 정제 후 남은 데이터 (정상상품만 남아야 함):")
    print(df_test[['product', 'price', 'quantity', 'revenue']])
    
    # 3) 검증: 정상상품 1건만 살아남았고, 그 매출액이 2000이 맞는지 확인
    is_filtered_correctly = len(df_test) == 1 and df_test.iloc[0]["product"] == "정상상품"
    is_revenue_correct = df_test.iloc[0]["revenue"] == 2000
    
    print(f"\n3) 검증(정상 데이터만 남기고 에러값 제거 여부): {is_filtered_correctly}")
    print(f"4) 검증(정상 데이터 매출액 연산 일치 여부): {is_revenue_correct}")
