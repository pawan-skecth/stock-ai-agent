from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

def analyze_news(stock_name, news_text):

    prompt = f"""
    You are a professional stock market news analyst.

    Analyze the following news for {stock_name}.

    News:
    {news_text}

    Give:
    1. News Summary
    2. Sentiment (Positive/Negative/Neutral)
    3. Impact on Stock
    """

    response = llm.invoke(prompt)

    return response.content