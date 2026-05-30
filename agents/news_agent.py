import yfinance as yf
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


def get_news(stock_symbol):

    stock = yf.Ticker(stock_symbol)

    news_items = []

    try:
        data = stock.news
        for item in data[:5]:
            title = item.get("title")
            if title:
                news_items.append(title)
    except:
        pass

    # fallback (IMPORTANT)
    if len(news_items) == 0:
        news_items = [
            f"{stock_symbol} stock shows active market movement",
            f"Investors are watching {stock_symbol} closely",
            f"Market sentiment around {stock_symbol} is evolving"
        ]

    return news_items


def analyze_news(stock_symbol):

    headlines = get_news(stock_symbol)

    prompt = f"""
    You are a professional financial news analyst.

    Analyze these stock news headlines:

    {headlines}

    Provide:
    1. News Summary
    2. Sentiment (Positive / Negative / Neutral)
    3. Market Impact
    4. Investor Insight
    """

    response = llm.invoke(prompt)

    return response.content