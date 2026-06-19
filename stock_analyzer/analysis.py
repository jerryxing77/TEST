from __future__ import annotations

from statistics import mean

from .models import NewsItem, Quote


def rank_movers(quotes: list[Quote]) -> list[Quote]:
    return sorted(quotes, key=lambda q: abs(q.change_percent), reverse=True)


def market_breadth(quotes: list[Quote]) -> dict[str, float | int]:
    if not quotes:
        return {"advancers": 0, "decliners": 0, "unchanged": 0, "average_change_percent": 0.0}
    advancers = sum(q.change_percent > 0 for q in quotes)
    decliners = sum(q.change_percent < 0 for q in quotes)
    return {
        "advancers": advancers,
        "decliners": decliners,
        "unchanged": len(quotes) - advancers - decliners,
        "average_change_percent": round(mean(q.change_percent for q in quotes), 2),
    }


def average_sentiment(news: list[NewsItem]) -> float:
    return round(mean(item.sentiment for item in news), 3) if news else 0.0


def risk_flags(quotes: list[Quote], news: list[NewsItem]) -> list[str]:
    flags: list[str] = []
    for quote in quotes:
        if abs(quote.change_percent) >= 5:
            flags.append(f"{quote.symbol} 单日波动 {quote.change_percent:.2f}%，需核查事件驱动因素")
        if quote.volume and quote.volume > 100_000_000:
            flags.append(f"{quote.symbol} 成交量显著放大：{quote.volume:,}")
    if average_sentiment(news) < -0.2:
        flags.append("新闻情绪偏负，盘前需降低追高仓位")
    return flags
