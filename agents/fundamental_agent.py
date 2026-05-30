import yfinance as yf


def fundamental_analysis(symbol):

    try:

        stock = yf.Ticker(symbol)

        info = stock.info

        pe_ratio = info.get("trailingPE", "N/A")
        eps = info.get("trailingEps", "N/A")
        market_cap = info.get("marketCap", "N/A")
        book_value = info.get("bookValue", "N/A")
        dividend_yield = info.get("dividendYield", "N/A")
        fifty_two_week_high = info.get("fiftyTwoWeekHigh", "N/A")
        fifty_two_week_low = info.get("fiftyTwoWeekLow", "N/A")

        analysis = f"""
PE Ratio: {pe_ratio}
EPS: {eps}
Market Cap: {market_cap}
Book Value: {book_value}
Dividend Yield: {dividend_yield}
52 Week High: {fifty_two_week_high}
52 Week Low: {fifty_two_week_low}
"""

        return analysis

    except Exception as e:

        return f"Fundamental Analysis Error: {str(e)}"