from typing import TypedDict


class StockState(TypedDict):

    stock_symbol: str

    stock_data: dict

    fundamental_data: str

    technical_data: dict

    risk_data: dict

    news_data: str

    sentiment_data: str

    strategy: str

    analysis: str