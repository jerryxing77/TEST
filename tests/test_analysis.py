from datetime import datetime, timezone

from stock_analyzer.analysis import average_sentiment, market_breadth, rank_movers, risk_flags
from stock_analyzer.models import NewsItem, Quote


def quote(symbol: str, price: float, previous: float, volume: int = 1_000) -> Quote:
    return Quote(symbol, price, previous, None, None, None, volume, "USD", datetime.now(timezone.utc))


def test_market_breadth_and_rank_movers():
    quotes = [quote("AAA", 110, 100), quote("BBB", 95, 100), quote("CCC", 100, 100)]
    assert market_breadth(quotes) == {"advancers": 1, "decliners": 1, "unchanged": 1, "average_change_percent": 1.67}
    assert [q.symbol for q in rank_movers(quotes)] == ["AAA", "BBB", "CCC"]


def test_sentiment_and_risk_flags():
    news = [NewsItem("AAA", "bad", "unit", "", datetime.now(timezone.utc), -0.5)]
    flags = risk_flags([quote("AAA", 106, 100, 120_000_000)], news)
    assert average_sentiment(news) == -0.5
    assert any("AAA 单日波动" in flag for flag in flags)
    assert any("成交量显著放大" in flag for flag in flags)
    assert any("新闻情绪偏负" in flag for flag in flags)
