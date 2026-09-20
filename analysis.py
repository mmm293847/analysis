import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# 삼성전자 주가 데이터 가져오기
df = yf.download(
    "005930.KS",
    start="2023-01-01",
    end="2026-01-01",
    auto_adjust=False
)

# 데이터 저장
df.to_csv("data/samsung_stock_2023_2025.csv")

# 데이터 기본 정보 확인
print("데이터 개수:", len(df))
print()
print("데이터 기간:")
print(df.index.min(), "~", df.index.max())
print()
print("데이터 컬럼:")
print(df.columns)
print()
print("결측치 개수:")
print(df.isnull().sum())

import matplotlib.pyplot as plt

# 20일 이동평균 계산
df["MA20"] = df["Close"].rolling(window=20).mean()

# 주가 + 이동평균 그래프
plt.figure(figsize=(12, 6))

plt.plot(df.index, df["Close"], label="Close Price")
plt.plot(df.index, df["MA20"], label="20-Day Moving Average")

plt.title("Samsung Electronics Stock Price and 20-Day Moving Average")
plt.xlabel("Date")
plt.ylabel("Price (KRW)")
plt.legend()
plt.grid(True)

plt.tight_layout()

# 그래프 저장
plt.savefig("images/02_moving_average.png", dpi=150)

plt.show()

# 일간 변화율 계산
df["Daily_Return"] = df["Close"].pct_change() * 100

# 가장 크게 상승한 날과 하락한 날 확인
max_increase = df["Daily_Return"].idxmax()
max_decrease = df["Daily_Return"].idxmin()

print()
print("가장 크게 상승한 날:")
print(max_increase, f"{df.loc[max_increase, 'Daily_Return']:.2f}%")

print()
print("가장 크게 하락한 날:")
print(max_decrease, f"{df.loc[max_decrease, 'Daily_Return']:.2f}%")

# 일간 변화율 그래프
plt.figure(figsize=(12, 6))

plt.plot(df.index, df["Daily_Return"])

plt.axhline(0, linewidth=1)

plt.title("Samsung Electronics Daily Return (2023-2025)")
plt.xlabel("Date")
plt.ylabel("Daily Return (%)")
plt.grid(True)

plt.tight_layout()

# 그래프 저장
plt.savefig("images/03_daily_return.png", dpi=150)

plt.show()

# 월별 수익률 계산
monthly_return = df["Close"]["005930.KS"].resample("ME").last().pct_change() * 100

print()
print("월별 수익률:")
print(monthly_return)

# 월별 수익률 그래프
plt.figure(figsize=(12, 6))

plt.bar(monthly_return.index, monthly_return.values)

plt.axhline(0, linewidth=1)

plt.title("Samsung Electronics Monthly Return (2023-2025)")
plt.xlabel("Date")
plt.ylabel("Monthly Return (%)")
plt.grid(True, axis="y")

plt.tight_layout()

# 그래프 저장
plt.savefig("images/04_monthly_return.png", dpi=150)

plt.show()

# 20일 이동 변동성 계산
df["Volatility_20"] = df["Daily_Return"].rolling(window=20).std()

# 가장 변동성이 높았던 날짜
max_volatility_date = df["Volatility_20"].idxmax()
max_volatility = df.loc[max_volatility_date, "Volatility_20"]

print()
print("가장 높은 20일 변동성이 나타난 시점:")
print(max_volatility_date)
print(f"20일 변동성: {max_volatility:.2f}%")

# 변동성 그래프
plt.figure(figsize=(12, 6))

plt.plot(df.index, df["Volatility_20"])

plt.title("Samsung Electronics 20-Day Rolling Volatility (2023-2025)")
plt.xlabel("Date")
plt.ylabel("Volatility (%)")
plt.grid(True)

plt.tight_layout()

# 그래프 저장
plt.savefig("images/05_volatility.png", dpi=150)

plt.show()

# 2024년 8월 5일 전후 주가 흐름 확인
event_date = "2024-08-05"

event_period = df.loc["2024-07-15":"2024-08-30"]

plt.figure(figsize=(12, 6))

plt.plot(
    event_period.index,
    event_period["Close"]["005930.KS"]
)

plt.axvline(
    pd.Timestamp(event_date),
    linestyle="--",
    linewidth=1
)

plt.title("Samsung Electronics Stock Price Around 2024-08-05")
plt.xlabel("Date")
plt.ylabel("Price (KRW)")
plt.grid(True)

plt.tight_layout()

plt.savefig("images/06_event_analysis.png", dpi=150)

plt.show()