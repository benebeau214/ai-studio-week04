# -*- coding: utf-8 -*-
"""
buggy_5.py  ―  '앞 행 대비 가격 변화'가 큰 행 찾기

정제한 price를 앞뒤로 비교하며 급변 지점을 찾으려 한다.
데이터에는 이상치(-4500, 9999999)도 섞여 있어 변화폭이 튀는 구간이 있다.
그런데 반복문이 끝까지 가지 못하고 죽는다.

[과제] Traceback으로 예외 타입을 확인하라(힌트: 반복문 경계).
       print 디버깅이 500줄 출력을 뒤져야 한다면,
       디버거의 '조건부 중단점'(예: 조건식  i >= len(prices) - 2)을 걸어
       문제의 반복 지점에서 곧바로 멈춰 원인을 관찰한 뒤 수정하라.
"""
import pandas as pd

def load_prices(path):
    df = pd.read_csv(path, encoding="utf-8")
    df["price"] = (df["price"].astype(str)
                              .str.replace(",", "")
                              .str.replace("원", "")
                              .str.strip())
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    # 결측은 0으로 두고, 리스트로 변환해 순회한다
    return df["price"].fillna(0).tolist()

def find_big_jumps(prices, threshold=100000):
    jumps = []
    for i in range(len(prices) - 1): # FIXED: 반복문 범위를 len(prices) - 1로 수정해서 IndexError 방지
        diff = prices[i + 1] - prices[i]      # <-- 여기가 문제의 줄
        if abs(diff) >= threshold:
            jumps.append((i, prices[i], prices[i + 1], diff))
    return jumps

if __name__ == "__main__":
    prices = load_prices("dirty_sales.csv")
    jumps = find_big_jumps(prices)
    print(f"급변 지점 {len(jumps)}건")
    for row in jumps[:10]:
        print(row)

    # 회귀 없음 확인 및 정상 데이터 처리 증빙
    print("\n--테스트--")
    # 1) 가상의 테스트 가격 리스트 생성 (정상적인 변화와 급변 구간 포함)
    test_prices = [1000, 2000, 150000, 151000]
    
    # 2) 수정한 함수 실행 (threshold=100000 기준)
    # 인덱스 1(2000)에서 인덱스 2(150000)로 갈 때 차이가 148,000이므로 1건이 검출되어야 함
    test_jumps = find_big_jumps(test_prices, threshold=100000)
    
    print(f"1) 테스트 가격 데이터: {test_prices}")
    print(f"2) 검출된 급변 지점: {test_jumps}")
    
    # 3) 검증: 스크립트가 멈추지 않고 끝까지 돌았는지, 검출 내역이 정확한지 확인
    is_completed_without_error = True 
    is_jump_correct = len(test_jumps) == 1 and test_jumps[0][3] == 148000
    
    print(f"3) 검증(마지막 인덱스에서 IndexError 발생 안 함): {is_completed_without_error}")
    print(f"4) 검증(급변 지점 1건 정상 검출 및 차액 일치 여부): {is_jump_correct}")