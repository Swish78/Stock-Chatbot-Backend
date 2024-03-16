import json
import openai
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf


def get_stock_price(ticker, period='1y'):
    """
    Get the latest closing price of a stock.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        str: The latest closing price of the stock.
    """
    try:
        stock_data = yf.Ticker(ticker).history(period=period)
        latest_price = stock_data.iloc[-1].Close
        return str(latest_price)
    except Exception as e:
        return f"Error fetching stock price for {ticker}: {str(e)}"


def get_stock_volume(ticker):
    """
    Get the historical volume data for a stock.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        str: The historical volume data for the stock.
    """
    try:
        stock_data = yf.Ticker(ticker).history(period='max')
        volume_data = stock_data['Volume'].to_dict()
        return str(volume_data)
    except Exception as e:
        return f"Error fetching stock volume for {ticker}: {str(e)}"


def calculate_sma(ticker,period='1y', window=50):
    """
    Calculate the Simple Moving Average (SMA) for a given stock.

    Args:
        ticker (str): The stock ticker symbol.
        period (str): The time period for which to fetch the stock data (e.g., '1y', '6m', '1d').
        window (int): The window size for the SMA calculation (e.g., 20, 50, 200).

    Returns:
        str: The calculated SMA value for the given stock and time period.
    """
    try:
        stock_data = yf.Ticker(ticker).history(period=period)
        sma = stock_data['Close'].rolling(window=window).mean().iloc[-1]
        return str(sma)
    except Exception as e:
        return f"Error calculating SMA for {ticker}: {str(e)}"


def calculate_ema(ticker,period='1y' ,window=50):
    """
    Calculate the (EMA) for a given stock.

    Args:
        ticker (str): The stock ticker symbol.
        period (str): The time period for which to fetch the stock data (e.g., '1y', '6m', '1d').
        window (int): The window size for the SMA calculation (e.g., 20, 50, 200).

    Returns:
        str: The calculated SMA value for the given stock and time period.
    """
    try:
        stock_data = yf.Ticker(ticker).history(period=period)
        ema = stock_data['Close'].rolling(span=window, adjust=False).mean().iloc[-1]
        return str(ema)
    except Exception as e:
        return f"Error calculating SMA for {ticker}: {str(e)}"


def calculate_rsi(ticker, window=14):
    """
    Calculate the Relative Strength Index (RSI) for a given stock.

    Args:
        ticker (str): The stock ticker symbol.
        window (int): The window size for RSI calculation (default is 14).

    Returns:
        str: The calculated RSI value for the given stock.
    """
    try:
        stock_data = yf.Ticker(ticker).history(period='1y')
        delta = stock_data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return str(rsi.iloc[-1])
    except Exception as e:
        return f"Error calculating RSI for {ticker}: {str(e)}"


def calculate_macd(ticker, short_window=12, long_window=26, signal_window=9):
    """
    Calculate the Moving Average Convergence Divergence (MACD) for a given stock.

    Args:
        ticker (str): The stock ticker symbol.
        short_window (int): The short window size (default is 12).
        long_window (int): The long window size (default is 26).
        signal_window (int): The signal window size (default is 9).

    Returns:
        str: The MACD value for the given stock.
    """
    try:
        stock_data = yf.Ticker(ticker).history(period='1y')
        short_ema = stock_data['Close'].ewm(span=short_window, min_periods=1, adjust=False).mean()
        long_ema = stock_data['Close'].ewm(span=long_window, min_periods=1, adjust=False).mean()
        macd = short_ema - long_ema
        signal_line = macd.ewm(span=signal_window, min_periods=1, adjust=False).mean()
        macd_histogram = macd - signal_line
        return str(macd_histogram.iloc[-1])
    except Exception as e:
        return f"Error calculating MACD for {ticker}: {str(e)}"


def plot_stock_price(ticker, period='1y'):
    """
    Plot the historical stock prices for a given stock.

    Args:
        ticker (str): The stock ticker symbol.
        period (str): The time period for which to fetch the stock data (default is '1y').
    """
    stock_data = get_stock_price(ticker, period)
    if stock_data is not None:
        plt.figure(figsize=(10, 6))
        plt.plot(stock_data.index, stock_data['Close'], label=f'{ticker} Close Price')
        plt.title(f'{ticker} Stock Price')
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.legend()
        plt.grid(True)
        plt.savefig(f'{ticker}.png')
        plt.close()


function_metadata = {
    "get_stock_price": {
        "name": "get_stock_price",
        "description": "Get the latest closing price of a stock.",
        "parameters": {
            "ticker": {
                "type": "str",
                "description": "The stock ticker symbol."
            },
            "period": {
                "type": "str",
                "description": "The time period for which to fetch the stock data (default is '1y')."
            }
        }
    },
    "get_stock_volume": {
        "name": "get_stock_volume",
        "description": "Get the historical volume data for a stock.",
        "parameters": {
            "ticker": {
                "type": "str",
                "description": "The stock ticker symbol."
            }
        }
    },
    "calculate_sma": {
        "name": "calculate_sma",
        "description": "Calculate the Simple Moving Average (SMA) for a given stock.",
        "parameters": {
            "ticker": {
                "type": "str",
                "description": "The stock ticker symbol."
            },
            "window": {
                "type": "int",
                "description": "The window size for the SMA calculation."
            }
        }
    },
    "calculate_ema": {
        "name": "calculate_ema",
        "description": "Calculate the Exponential Moving Average (EMA) for a given stock.",
        "parameters": {
            "ticker": {
                "type": "str",
                "description": "The stock ticker symbol."
            },
            "window": {
                "type": "int",
                "description": "The window size for the EMA calculation."
            }
        }
    },
    "calculate_rsi": {
        "name": "calculate_rsi",
        "description": "Calculate the Relative Strength Index (RSI) for a given stock.",
        "parameters": {
            "ticker": {
                "type": "str",
                "description": "The stock ticker symbol."
            },
            "window": {
                "type": "int",
                "description": "The window size for RSI calculation (default is 14)."
            }
        }
    },
    "calculate_macd": {
        "name": "calculate_macd",
        "description": "Calculate the Moving Average Convergence Divergence (MACD) for a given stock.",
        "parameters": {
            "ticker": {
                "type": "str",
                "description": "The stock ticker symbol."
            },
            "short_window": {
                "type": "int",
                "description": "The short window size (default is 12)."
            },
            "long_window": {
                "type": "int",
                "description": "The long window size (default is 26)."
            },
            "signal_window": {
                "type": "int",
                "description": "The signal window size (default is 9)."
            }
        }
    }
}


function_mapping = {
    "get_stock_price": get_stock_price,
    "get_stock_volume": get_stock_volume,
    "calculate_sma": calculate_sma,
    "calculate_ema": calculate_ema,
    "calculate_rsi": calculate_rsi,
    "calculate_macd": calculate_macd
}

# gpt-3.5-turbo-0125

# sma_50 = calculate_sma('AAPL', '1y', 50)
# print(f"50-day SMA for AAPL: {sma_50}")