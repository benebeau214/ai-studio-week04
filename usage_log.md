# 진단 보고

## buggy_1.py

ValueError가 line 19 price = int(row["price"]) 코드에서 일어남. 

에러 메시지를 보면 'invalid literal for int() with base 10: '5,200'으로, int형으로 변환하려 했으나 값에 콤마(,)가 중간에 있어서 int형 변환에 실패함.

replace()를 사용해 row["price"]의 값들에 있는 콤마를 제거하고 실행하니 price = int(row["price"]) 코드에서 ValueError: invalid literal for int() with base 10: '4200원' 이라는 ValueError 에러 메시지가 나옴. 값에 '원'이 포함되어있어서 int형 변환에 실패함.

replace()를 사용해 '원' 문자를 제거하고 실행하니 price = int(row["price"]) 코드에서 ValueError: invalid literal for int() with base 10: '' 라는 ValueError 에러 메시지가 나옴.

''(빈 문자열)을 int형으로 변환하려고 해서 실패하고 있음.

## buggy_2.py

KeyError가 line 20 df["매출액"] = df["단가"] * df["수량"] 코드에서 일어남. 에러 메시지를 보면 'KeyError: '단가''로, dirty_sales.csv를 육안으로 확인했을 때 '단가'라는 컬럼명 자체가 없어서 존재 하지 않는 Key에 접근하려고 해서 Error가 나는 것으로 확인됨. 같은 코드 라인의 '수량'도 마찬가지로 존재하지 않는 Key 값으로 KeyError를 일으키는 부분임.

## buggy_3.py

AttributeError가 line 28 result = df.groupby("category")["revenue"].sum() 코드에서 일어남. 에러 메시지를 보면 'AttributeError: 'NoneType' object has no attribute 'groupby''로, groupby의 인자로 들어온 값 중 NoneType이 있어서 에러가 나는 것으로 확인됨. 인자로 들어온 'category'는 dirty_sales.csv 파일에 기존에 있던 컬럼명이기 때문에 문제가 되는 부분은 'revenue' 인자임. 'revenue' 인자를 만드는 부분은 def load_and_clean() 함수로, 함수가 revenue가 추가된 df를 반환하지 않아서 main()에서 revenue가 없는 df에 groupby 메소드로 revenue에 접근하려해서 에러가 일어남.

## buggy_4.py

df.info()와 df[["price", "quantity", "revenue"]].describe() 메소드를 사용해 다음과 같은 데이터 구조와 컬럼의 통계를 확인하였다.

```python
[전체 데이터 구조]
<class 'pandas.DataFrame'>
RangeIndex: 500 entries, 0 to 499
Data columns (total 7 columns):
 #   Column    Non-Null Count  Dtype  
---  ------    --------------  -----  
 0   date      500 non-null    str    
 1   product   500 non-null    str    
 2   category  490 non-null    str    
 3   price     498 non-null    float64
 4   quantity  500 non-null    int64  
 5   stock     485 non-null    float64
 6   revenue   498 non-null    float64
dtypes: float64(3), int64(1), str(3)
memory usage: 27.5 KB

[price, quantity, revenue 컬럼 통계]
              price      quantity       revenue
count  4.980000e+02  5.000000e+02  4.980000e+02
mean   2.834237e+04  2.010569e+04  3.036112e+08
std    4.477810e+05  4.472088e+05  6.721638e+09
min   -4.500000e+03  1.000000e+00 -5.355000e+05
25%    3.800000e+03  5.375000e+01  2.789250e+05
50%    5.000000e+03  1.120000e+02  5.787500e+05
75%    1.200000e+04  1.610000e+02  9.833750e+05
max    9.999999e+06  9.999999e+06  1.500000e+11
```

매출액을 집계하는데 쓰이는 price와 quantity의 개수가 498개와 500개로 price가 quantity의 데이터 개수보다 2개 적어 결측치가 2건 있는것으로 예상이 되었다. 이를 확인하고자 df.isna().sum() 함수를 출력하였고,

```python
[컬럼별 결측건수 통계]

date         0

product      0

category    10

price        2

quantity     0

stock       15

revenue      2
```

위와 같이 예상한 바와 같이 price에 결측치가 2건 있는 것을 확인하였다.

또한 컬럼 통계 결과를 보았을 때 price의 min, max 값이 -4500과 9999999, quantity의 max 값이 9999999으로 다른 데이터 값들과는 값이 매우 다르게 튀는 이상치가 있는 것을 확인하였다. 이러한 이상치와 결측치로 인해 revenue에도 결측치가 2건 있고, min 값도 -535500 이라는 음수값으로 집계가 제대로 되지 않은 상태이다.

## buggy_5.py

IndexError가 line 29 diff = prices[i + 1] - prices[i] 코드에서 일어남. 에러 메시지를 보면 ‘IndexError: list index out of range’로, 접근하려는 인덱스가 유효 범위에서 벗어난 것을 알 수 있음.

에러가 일어나는 line 29에 조건부 중단점으로 i >= len(prices) - 2 수식을 걸어서 디버깅함.

debug console에서 i, i + 1, len(prices) 값을 확인한 결과

i = 499, i + 1 = 500, len(prices) = 500 임을 확인함.

len(prices)가 500인데 0부터 index가 시작하므로 마지막 유효 인덱스는 499이다.

그러나  diff = prices[i + 1] - prices[i] 에서 i + 1로 유효하지 않은 인덱스인 500에 접근하므로 IndexError가 발생하는 것을 알 수 있다.

# AI 사용 기록

## buggy_1.py

AI 미사용

## buggy_2.py

### 사용 프롬프트

카테고리별로 매출을 집계하는 스크립트야.

```python
def summarize(df):

# 단가 x 수량으로 매출액 컬럼을 만든 뒤 카테고리별 합계를 낸다

df["매출액"] = df["단가"] * df["수량"]

return df.groupby("category")["매출액"].sum()
```

summarize 함수의 df["매출액"] = df["단가"] * df["수량"] 이 코드라인에서

```python
Traceback (most recent call last):

File "C:\dev\ai_studio\ai-studio-week04\buggy_2.py", line 25, in <module>

result = summarize(df)

File "C:\dev\ai_studio\ai-studio-week04\buggy_2.py", line 20, in summarize

df["매출액"] = df["단가"] * df["수량"]        # <-- 여기가 문제의 줄

~~^^^^^^^^

File "C:\Users\kimrn\AppData\Local\Programs\Python\Python313\Lib\site-packages\pandas\core\frame.py", line 4378, in __**getitem**__

indexer = self.columns.get_loc(key)

File "C:\Users\kimrn\AppData\Local\Programs\Python\Python313\Lib\site-packages\pandas\core\indexes\base.py", line 3648, in get_loc

raise KeyError(key) from err

KeyError: '단가'
```

이러한 KeyError가 일어나. 내가 csv 파일을 확인했을 때 컬럼명 자체가 단가, 수량이 아니라

price, quantity로 되어있어서 KeyError가 일어나는 거 같아.

내 가설이 맞는지 검증하는 코드를 작성해줘.

### AI 답변

다음 검증 코드를 summarize(df) 호출 전에 넣어 보세요.

```python
if __name__ == "__main__":
    df = load("dirty_sales.csv")

    print("실제 컬럼명:", df.columns.tolist())

    required_columns = ["단가", "수량"]
    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        print("존재하지 않는 컬럼:", missing_columns)
        print("사용 가능한 컬럼:", df.columns.tolist())
    else:
        print("단가와 수량 컬럼이 모두 존재합니다.")

    print("\n데이터 미리보기:")
    print(df.head())
```

### AI 답변 채택 여부와 판단 이유

채택하였다. 왜냐하면 실제 존재해서 Key 값으로 사용할 수 있는 컬럼명과 Traceback과 csv 파일을 확인한 결과 존재하지 않는 것으로 확인되는 '단가'와 '수량' 컬럼을 확인할 수 있기 때문이다.

### 검증 결과

AI가 제공해준 검증 코드를 실행한 출력 결과는 다음과 같다.

```python
실제 컬럼명: ['date', 'product', 'category', 'price', 'quantity', 'stock']

존재하지 않는 컬럼: ['단가', '수량']

사용 가능한 컬럼: ['date', 'product', 'category', 'price', 'quantity', 'stock']
```

'단가'와 '수량'이 존재하지 않는 것을 확인할 수 있다. 그러므로 실제 존재하는 컬럼명 중 'price'와 'quantity'를 사용해야 한다.

## buggy_3.py

미사용

## buggy_4.py

### 사용 프롬프트

내가 수정하려는 스크립트는 dirty_sales.csv의 총 매출액을 집계하는 스크립트야.

dirty_sales.csv의 컬럼은 date, product, category, price, quantity, stock으로 이루어져있어.

info()와 describe(), df.isna().sum()를 사용해서 데이터 상태를 확인해 보니

```python
[전체 데이터 구조]
<class 'pandas.DataFrame'>
RangeIndex: 500 entries, 0 to 499
Data columns (total 7 columns):
 #   Column    Non-Null Count  Dtype  
---  ------    --------------  -----  
 0   date      500 non-null    str    
 1   product   500 non-null    str    
 2   category  490 non-null    str    
 3   price     498 non-null    float64
 4   quantity  500 non-null    int64  
 5   stock     485 non-null    float64
 6   revenue   498 non-null    float64
dtypes: float64(3), int64(1), str(3)
memory usage: 27.5 KB

[price, quantity, revenue 컬럼 통계]
              price      quantity       revenue
count  4.980000e+02  5.000000e+02  4.980000e+02
mean   2.834237e+04  2.010569e+04  3.036112e+08
std    4.477810e+05  4.472088e+05  6.721638e+09
min   -4.500000e+03  1.000000e+00 -5.355000e+05
25%    3.800000e+03  5.375000e+01  2.789250e+05
50%    5.000000e+03  1.120000e+02  5.787500e+05
75%    1.200000e+04  1.610000e+02  9.833750e+05
max    9.999999e+06  9.999999e+06  1.500000e+11

[컬럼별 결측건수 통계]

date         0

product      0

category    10

price        2

quantity     0

stock       15

revenue      2
```

위와 같이 나왔고 매출액 계산에 영향을 주는 price에서 결측치가 2건이 있어. 이로 인해 price*quantity로 생성된 revenue도 데이터가 500개가 생겨야 하는데 498개만 생겼어.

그리고 price의 min값이 -4500, max가 9999999야. quantity의 max도 9999999라서 파일에 기록된 데이터들 보다 극단적으로 값이 크거나 양수 값이어야 하는데 음수인 상황이야.

이러한 결측치와 이상치를 처리하는 방법을 알려줘

### AI 답변

1. 결측치 처리

전체 500개의 데이터 중 단 2개(0.4%)에만 결측치가 존재하므로, 해당 행을 삭제(Drop)하는 것이 가장 깔끔하고 안전합니다.

2. 이상치(Outlier) 처리

음수 가격 제거: price는 현실적으로 0보다 커야 하므로 price > 0 조건으로 필터링합니다.

극단값 더미(9999999) 제거: 9999999는 시스템에서 임의로 채워 넣은 더미(Dummy) 값이거나 오타일 확률이 100%에 가깝습니다. 정상적인 범위를 벗어나는 이 값들을 조건문으로 제외합니다.

### AI 답변 채택 여부와 판단 이유

AI 답변을 채택하여 결측치와 이상치를 제거하였다. 왜냐하면 price에는 결측치가 2건, 이상치가 2건이 존재하고 quantity에서는 이상치가 1건 존재함으로 전체 데이터 규모에 비해 결측치와 이상치의 개수가 매우 적기 때문에 데이터를 평균이나 중앙값, 직전 값으로 대체하는 작업을 하지 않고 삭제하는 방향으로 처리하였다.

### 검증 결과

<수정 전>

총 매출액: 151,198,388,824원

평균 단가: 28,342원

<수정 후>

총 매출액: 438,939,400원

평균 단가: 8,291원

결측치와 이상치를 제거하는 코드를 추가하여서 총 매출액과 평균 단가의 결과가 달라지게 되었다. 또한 자체적으로 추가한 테스트 코드를 실행하였을 때,

```python
--테스트--
1) 테스트 원본 데이터:
  product    price  quantity
0    정상상품     1000         2
1    결측상품      NaN         1
2    음수상품     -500         1
3  극단값상품1  9999999         1
4  극단값상품2     2000   9999999

2) 정제 후 남은 데이터 (정상상품만 남아야 함):
  product   price  quantity  revenue
0    정상상품  1000.0         2   2000.0

3) 검증(정상 데이터만 남기고 에러값 제거 여부): True
4) 검증(정상 데이터 매출액 연산 일치 여부): True
```

위와 같이 나오는 것으로, 결측치와 이상치를 제거하는 코드가 정상적으로 실행되는 것을 검증하였다.

## buggy_5.py

미사용

# AI에게 수정한 코드 설명 요구

## buggy_4.py

### 사용한 프롬프트

이 스크립트는 총 매출액을 집계하는 스크립트야. 주석으로 #FIXED 표시된 부분이 내가 수정한 부분이야. 내가 수정한 부분의 코드에 대해 설명해줘 

```python
    # 수정 코드
    df = df.dropna(subset=["price"])  # FIXED : 결측값 제거
    df = df[df["price"] > 0]  # FIXED : 음수 가격 제거
    df = df[df["price"] < 9999999]  # FIXED : 극단적인 이상치 제거
    df = df[df["quantity"] < 9999999] # FIXED : 극단적인 이상치 제거
```

### AI 답변

작성해주신 코드는 데이터 분석에서 가장 무서운 '에러 없이 조용히 틀리는' 문제를 아주 잘 짚어내고 해결했습니다. 수정하신 4줄의 코드가 왜 중요한지, 데이터의 어떤 문제를 방지하는지 하나씩 설명해 드릴게요.

- **`df = df.dropna(subset=["price"])` (결측값 제거)**
    - 앞선 코드에서 `errors="coerce"` 옵션을 사용했기 때문에, 숫자로 바꿀 수 없는 이상한 문자열이나 비어있는 값은 모두 `NaN`(결측치)으로 변환된 상태입니다.
    - `.sum()` 함수가 `NaN`을 조용히 무시하고 덧셈을 해주긴 하지만, 결측치를 명시적으로 날려버리지 않으면 나중에 `df["price"].mean()`처럼 평균 단가를 구할 때 분모(전체 데이터 개수)가 꼬여서 평균값이 왜곡됩니다. 분석의 기본이 되는 아주 깔끔한 조치입니다.
- **`df = df[df["price"] > 0]` (음수 및 0원 가격 제거)**
    - 현실의 판매 데이터에서 단가가 마이너스(-)인 경우는 보통 반품(Refund), 취소 건이거나 시스템 입력 오류입니다. 단가가 0원인 경우는 사은품일 수 있습니다.
    - 이것을 그대로 두면 정상적인 매출액에서 반품액이나 에러값이 깎여버리거나 평균 단가 계산이 망가집니다. 0보다 큰 정상적인 가격만 남겨서 '순수 판매 매출'만 정확히 집계하도록 잘 통제했습니다.
- **`df = df[df["price"] < 9999999]` (단가 극단적 이상치 제거)**
    - `9999999` 같은 숫자는 과거 시스템을 테스트할 때 넣은 더미 데이터이거나, 가격을 모를 때 입력 담당자가 대충 키보드를 두드려 채워 넣은 전형적인 '가짜 값'입니다.
    - 이 값이 그대로 수량과 곱해지면 총 매출액이 순식간에 비정상적으로 뻥튀기되어 전체 통계가 완전히 오염됩니다. 이 필터링 덕분에 데이터의 신뢰도가 크게 올라갔습니다.
- **`df = df[df["quantity"] < 9999999]` (수량 극단적 이상치 제거)**
    - 단가와 마찬가지로 수량에 들어갈 수 있는 더미 값도 차단했습니다.
    - 만약 단가가 정상적인 5,000원이더라도 수량이 9,999,999개로 입력되어 있다면, 그 단 한 줄의 에러 데이터 때문에 500억 원의 가짜 매출이 총액에 더해지게 됩니다. 양쪽 모두에서 이상치를 방어한 것은 훌륭한 접근입니다.

### 답변 검증

buggy_4.py에서 수정한 코드의 설명이 정확했다.

price에서는 콤마나 ‘원’ 문자가 섞인 값이 섞여있기 때문에 errors=”coerce” 옵션으로 NaN이 되어버린 값들을 제거하고,

price에서 음수값과 극단값, quantity에서 극단값이 존재했기에 이러한 이상치를 제거해주는 전처리 코드를 넣은 것이 맞기 때문에 의도를 파악해서 정확한 설명이 제공되었다.