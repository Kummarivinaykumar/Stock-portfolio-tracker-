# portfolio/utils.py

import yfinance as yf

def fetch_real_time_data(ticker):
    """Fetch real-time stock data for a given ticker."""
    try:
        stock = yf.Ticker(ticker)
        stock_data = stock.history(period='1d')
        
        if stock_data.empty:
            return None  # No data available
        
        current_price = stock_data['Close'].iloc[-1]  # Get the latest closing price
        return {
            'ticker': ticker,
            'current_price': round(current_price, 2)
        }
    except Exception as e:
        print(f"Error fetching real-time data for {ticker}: {e}")
        return None

def fetch_historical_data(ticker, period="1d"):
    """Fetch historical stock data for a given ticker."""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        
        if hist.empty:
            return None  # No historical data available
        
        return {
            'dates': hist.index.strftime('%Y-%m-%d').tolist(),
            'prices': hist['Close'].tolist()
        }
    except Exception as e:
        print(f"Error fetching historical data for {ticker}: {e}")
        return None
