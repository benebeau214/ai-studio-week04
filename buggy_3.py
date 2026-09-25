# -*- coding: utf-8 -*-
"""
buggy_3.py  ―  데이터 로드 후 카테고리별 집계

load_and_clean()으로 데이터를 읽어 정제한 뒤,
그 결과를 groupby로 집계하려 한다.
그런데 집계 단계에서 이상한 에러가 난다.

[과제] Traceback의 예외 타입을 확인하고,
       'NoneType ...' 메시지가 가리키는 '이 변수를 만든 직전 단계'를
       역추적하여 원인 함수를 찾아 수정하라.
"""
import pandas as pd

def load_and_clean(path):
    df = pd.read_csv(path, encoding="utf-8")
    # price 컬럼을 숫자로 정제
    df["price"] = (df["price"].astype(str)
                              .str.replace(",", "")
                              .str.replace("원", "")
                              .str.strip())
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["revenue"] = df["price"] * df["quantity"]
    # (여기서 정제된 df를 돌려주려고 했는데...)   <-- 무언가 빠져 있다
    return df  # FIXED : 정제된 DataFrame을 반환하도록 수정

def main():
    df = load_and_clean("dirty_sales.csv")
    result = df.groupby("category")["revenue"].sum()   # <-- 여기서 죽는다
    print(result)

    # 회귀 없음 확인 및 정상 데이터 처리 증빙

    print("\n--테스트--")
    # 1. 정상적으로 정제된 상위 3개 행의 데이터 확인   
    print("1) price 정제 및 revenue 컬럼 생성 결과:")
    print(df[['price', 'quantity', 'revenue']].head(3))

    # 2. 첫 번째 행을 집어서 단가 * 수량 = 매출액 수식이 맞는지 확인
    sample = df.iloc[0]
    expected_revenue = sample['price'] * sample['quantity']
    print(f"\n2) 개별 정상 데이터 연산 확인:")
    print(f"단가(price): {sample['price']}")
    print(f"수량(quantity): {sample['quantity']}")
    print(f"실제 계산된 매출액(revenue): {sample['revenue']}")
    print(f"검증(단가 x 수량 일치 여부): {sample['revenue'] == expected_revenue}")

if __name__ == "__main__":
    main()
