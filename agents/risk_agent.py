import yfinance as yf
import numpy as np


def risk_analysis(symbol):

    try:

        df = yf.download(
            tickers=symbol,
            period="3mo",
            interval="1d",
            progress=False,
            auto_adjust=True,
            threads=False
        )

        # EMPTY CHECK
        if df is None or df.empty:
            return {
                "error": "No risk data found"
            }

        # FIX MULTIINDEX
        if hasattr(df.columns, "levels"):
            df.columns = df.columns.get_level_values(0)

        # CLOSE CHECK
        if "Close" not in df.columns:
            return {
                "error": "Close column missing"
            }

        returns = df["Close"].pct_change().dropna()

        volatility = np.std(returns)

        risk_level = "Low"

        if volatility > 0.03:
            risk_level = "Medium"

        if volatility > 0.06:
            risk_level = "High"

        return {
            "volatility": float(volatility),
            "risk_level": risk_level
        }

    except Exception as e:

        return {
            "error": str(e)
        }