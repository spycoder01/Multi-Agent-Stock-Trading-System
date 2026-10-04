import yfinance as yf
from crewai.tools import tool


@tool("Stock Research Tool")
def get_stock_data(symbol: str) -> str:
    """
    Fetch basic stock market information from Yahoo Finance.
    """

    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        current_price = info.get("currentPrice")
        previous_close = info.get("previousClose")
        market_cap = info.get("marketCap")
        volume = info.get("volume")
        fifty_two_week_high = info.get("fiftyTwoWeekHigh")
        fifty_two_week_low = info.get("fiftyTwoWeekLow")

        if current_price is None:
            return f"Could not find stock data for {symbol}."

        if previous_close:
            change = current_price - previous_close
            change_percent = (change / previous_close) * 100
        else:
            change = 0
            change_percent = 0

        return f"""
Stock Information for {symbol}

Current Price: {current_price}
Previous Close: {previous_close}
Daily Change: {change:.2f} ({change_percent:.2f}%)
Volume: {volume}
Market Cap: {market_cap}
52-Week High: {fifty_two_week_high}
52-Week Low: {fifty_two_week_low}
"""

    except Exception as e:
        return f"Error fetching stock data for {symbol}: {str(e)}"

