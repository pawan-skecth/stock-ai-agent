from langchain_groq import ChatGroq
from dotenv import load_dotenv
from utils.supabase_memory import save_memory, get_memory
import re

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


def final_strategy(stock_symbol, combined_data):

    if not combined_data:
        return "No data available"

    history = get_memory(stock_symbol)

    prompt = f"""
You are an expert AI Stock Market Analyst.

Analyze ALL the information provided.

CURRENT ANALYSIS DATA:
{combined_data}

PREVIOUS MEMORY:
{history}

IMPORTANT INSTRUCTIONS:

- Final Decision must appear at the VERY TOP.
- Mention ONLY ONE decision:
  BUY
  HOLD
  SELL

- You MUST analyze FUNDAMENTAL DATA.
- You MUST explain:
    - PE Ratio
    - EPS
    - Market Cap
    - Book Value
    - Dividend Yield
    - 52 Week High
    - 52 Week Low

- Explain whether the stock appears:
    - Undervalued
    - Fairly Valued
    - Overvalued

- You MUST analyze TECHNICAL DATA.
- You MUST analyze RISK DATA.
- You MUST analyze NEWS DATA.
- You MUST analyze SENTIMENT DATA.

- Mention Current Stock Price.

- If currency is INR display ₹.
- If currency is USD display $.

- Give a Confidence Score between 0 and 100.

RESPONSE FORMAT:

DECISION: BUY/HOLD/SELL

Current Stock Price:

Fundamental Analysis:

Technical Analysis:

Risk Analysis:

News & Sentiment Analysis:

Reason:

Confidence Score:
"""

    response = llm.invoke(prompt)

    output = response.content

    # -------------------------
    # EXTRACT DECISION
    # -------------------------

    decision = "HOLD"

    match = re.search(
        r"DECISION:\s*(BUY|HOLD|SELL)",
        output.upper()
    )

    if match:
        decision = match.group(1)

    # -------------------------
    # SAVE MEMORY
    # -------------------------

    save_memory(
        stock_symbol,
        decision,
        "N/A"
    )

    return output