from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

def sentiment_analysis(news_text):

    prompt = f"""
    You are a financial sentiment analyst.

    Analyze the sentiment of the following news:

    {news_text}

    Return:
    1. Sentiment (Positive / Negative / Neutral)
    2. Reason
    3. Impact on stock
    """

    response = llm.invoke(prompt)

    return response.content