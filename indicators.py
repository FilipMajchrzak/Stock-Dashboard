#Import necessary libraries
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


def fetch_data(ticker, years_back=2):
    """Fetch historical OHLCV data for a single ticker."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years_back * 365)
    data = yf.download(ticker, start=start_date, end=end_date, threads=False)
    return data


def calculate_moving_averages(close_prices, windows=[20, 50, 100]):
    """Return a dict of {window: moving_average_series}."""
    moving_averages = {}
    for window in windows:
        moving_averages[window] = close_prices.rolling(window=window).mean()
    return moving_averages


def calculate_rsi(close_prices, window=14):
    """RSI = 100 - (100 / (1 + RS)), RS = Average Gain / Average Loss."""
    delta = close_prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_bollinger_bands(close_prices, window=20, num_std=2):
    """Bollinger Bands = moving average ± (standard deviation * n)."""
    middle_band = close_prices.rolling(window=window).mean()
    std_dev = close_prices.rolling(window=window).std()
    upper_band = middle_band + (num_std * std_dev)
    lower_band = middle_band - (num_std * std_dev)
    return upper_band, middle_band, lower_band


def build_price_chart(ticker, years_back=2):
    """
    Build a single combined chart for a ticker: price + MAs + Bollinger Bands (top),
    RSI (middle), Volume (bottom). Returns a matplotlib Figure for Streamlit to display.
    """
    data = fetch_data(ticker, years_back=years_back)
    close_prices = data['Close'][ticker] if isinstance(data['Close'], type(data)) else data['Close']
    # yfinance single-ticker download can return a flat column, not a sub-frame
    if hasattr(data['Close'], 'columns'):
        close_prices = data['Close'][ticker]
    else:
        close_prices = data['Close']

    volume = data['Volume'][ticker] if hasattr(data['Volume'], 'columns') else data['Volume']

    moving_averages = calculate_moving_averages(close_prices)
    rsi = calculate_rsi(close_prices)
    upper_band, middle_band, lower_band = calculate_bollinger_bands(close_prices)

    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True,
                              gridspec_kw={'height_ratios': [3, 1, 1]})

    # --- Price + MAs + Bollinger Bands ---
    ax_price = axes[0]
    ax_price.plot(close_prices, label=f'{ticker} Close', color='blue')
    for window, ma in moving_averages.items():
        ax_price.plot(ma, label=f'{window}-Day MA', linestyle='--')
    ax_price.plot(upper_band, label='Upper Bollinger Band', color='red', linestyle=':')
    ax_price.plot(middle_band, label='Middle Bollinger Band', color='green', linestyle=':')
    ax_price.plot(lower_band, label='Lower Bollinger Band', color='orange', linestyle=':')
    ax_price.set_title(f'{ticker} Price, Moving Averages & Bollinger Bands')
    ax_price.set_ylabel('Price')
    ax_price.legend(loc='upper left', fontsize=8)

    # --- RSI ---
    ax_rsi = axes[1]
    ax_rsi.plot(rsi, label='RSI', color='orange')
    ax_rsi.axhline(70, color='red', linestyle='--', label='Overbought (70)')
    ax_rsi.axhline(30, color='green', linestyle='--', label='Oversold (30)')
    ax_rsi.set_ylabel('RSI')
    ax_rsi.legend(loc='upper left', fontsize=8)

    # --- Volume ---
    ax_vol = axes[2]
    ax_vol.bar(volume.index, volume, color='grey')
    ax_vol.set_ylabel('Volume')
    ax_vol.set_xlabel('Date')

    plt.tight_layout()
    return fig

