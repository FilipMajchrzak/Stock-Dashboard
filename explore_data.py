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

#RSI = 100 - (100 / (1 + RS))
#RS = Average Gain / Average Loss over n days

def calculate_rsi(close_prices, window=14):
    delta = close_prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

#Calculate RSI for each stock
all_rsi = {}
for ticker in tickers:
    close_prices = data['Close'][ticker]
    all_rsi[ticker] = calculate_rsi(close_prices)
    print(f"{ticker} RSI:\n", all_rsi[ticker].tail(5))


#plot RSI and closing prices for each ticker
for ticker in tickers:
    plt.figure(figsize=(14, 7))
    plt.subplot(2, 1, 1)
    plt.plot(data['Close'][ticker], label=f'{ticker} Close Price', color='blue')
    plt.title(f'{ticker} Stock Price')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(all_rsi[ticker], label=f'{ticker} RSI', color='orange')
    plt.axhline(70, color='red', linestyle='--', label='Overbought (70)')
    plt.axhline(30, color='green', linestyle='--', label='Oversold (30)')
    plt.title(f'{ticker} Relative Strength Index (RSI)')
    plt.xlabel('Date')
    plt.ylabel('RSI')
    plt.legend()
    
    plt.tight_layout()
    plt.show()

#Bollinger bands = moving average ± (standard deviation * n)

def calculate_bollinger_bands(close_prices, window=20, num_std=2):
    middle_band = close_prices.rolling(window=window).mean()
    std_dev = close_prices.rolling(window=window).std()
    
    upper_band = middle_band + (num_std * std_dev)
    lower_band = middle_band - (num_std * std_dev)
    
    return upper_band, middle_band, lower_band
for ticker in tickers:
    close_prices = data['Close'][ticker]
    upper_band, middle_band, lower_band = calculate_bollinger_bands(close_prices)
    
    plt.figure(figsize=(14, 7))
    plt.plot(close_prices, label=f'{ticker} Close Price', color='blue')
    plt.plot(upper_band, label='Upper Bollinger Band', color='red', linestyle='--')
    plt.plot(middle_band, label='Middle Bollinger Band', color='green', linestyle='--')
    plt.plot(lower_band, label='Lower Bollinger Band', color='orange', linestyle='--')
    
    plt.title(f'{ticker} Bollinger Bands')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()