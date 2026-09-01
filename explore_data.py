#Import necessary libraries
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

#Set the time frame for data extraction
years_back = 2
end_date = datetime.now()
start_date = end_date - timedelta(days=years_back * 365)

#Download historical stock data for NVDA, S&P 500, and NASDAQ
tickers = ["NVDA", "^GSPC", "^NDX"]
data = yf.download(tickers, start=start_date, end=end_date, threads=False)

#Print the columns of the downloaded data
print(data.columns)
nvda_close = data['Close']['NVDA']
print(nvda_close)

#Check for missing values in the data
print("Missing values in NVDA Close data:", nvda_close.isnull().sum())
print("Missing values in S&P 500 Close data:", data['Close']['^GSPC'].isnull().sum())
print("Missing values in NASDAQ Close data:", data['Close']['^NDX'].isnull().sum())

#Check data is in chronological order
if nvda_close.index.is_monotonic_increasing:
    print("NVDA Close data is in chronological order.")
if data['Close']['^GSPC'].index.is_monotonic_increasing:
    print("S&P 500 Close data is in chronological order.")
if data['Close']['^NDX'].index.is_monotonic_increasing:
    print("NASDAQ Close data is in chronological order.")

#Define a function to fetch and return the historical stock data for a given ticker
def fetch_data(tickers, years_back=2):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years_back * 365)
    data = yf.download(tickers, start=start_date, end=end_date, threads=False)
    return data

test_data = fetch_data(["NVDA", "^GSPC", "^NDX"], years_back=1)
print(test_data.tail())

#Define a function to calculate moving averages for a given stock's closing prices
def calculate_moving_averages(close_prices, windows=[20, 50, 100]):
    moving_averages = {}
    for window in windows:
        moving_averages[window] = close_prices.rolling(window=window).mean()
    return moving_averages

#Calculate moving averages for each stock
all_moving_averages = {}

for ticker in tickers:
    close_prices = data['Close'][ticker]
    all_moving_averages[ticker] = calculate_moving_averages(close_prices)

print(all_moving_averages["NVDA"][100].tail(5))
print(all_moving_averages["^GSPC"][20].tail(5))
print(all_moving_averages["^NDX"][50].tail(5))

#Plot the closing prices and moving averages for each ticker
for ticker in tickers:
    plt.figure(figsize=(14, 7))
    plt.plot(data['Close'][ticker], label=f'{ticker} Close Price', color='blue')
    for window, ma in all_moving_averages[ticker].items():
        plt.plot(ma, label=f'{ticker} {window}-Day MA', linestyle='--')
    plt.title(f'{ticker} Stock Price and Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()
