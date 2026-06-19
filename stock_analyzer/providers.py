from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Protocol
from urllib.parse import quote
from urllib.request import urlopen

from .models import NewsItem, Quote


class MarketDataProvider(Protocol):
    def get_quote(self, symbol: str) -> Quote: ...

    def get_news(self, symbol: str, limit: int = 5) -> list[NewsItem]: ...


class YahooChartProvider:
    """Small no-key provider using Yahoo Finance public chart endpoints."""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def _load_json(self, url: str) -> dict:
        with urlopen(url, timeout=self.timeout) as response:
            return json.loads(response.read().decode("utf-8"))

    def get_quote(self, symbol: str) -> Quote:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{quote(symbol)}?range=5d&interval=1d"
        payload = self._load_json(url)
        result = payload["chart"]["result"][0]
        meta = result["meta"]
        quote_data = result["indicators"]["quote"][0]
        closes = [v for v in result["indicators"].get("adjclose", [{}])[0].get("adjclose", []) if v is not None]
        previous_close = float(meta.get("chartPreviousClose") or (closes[-2] if len(closes) > 1 else closes[-1]))
        price = float(meta.get("regularMarketPrice") or closes[-1])
        idx = -1
        ts = datetime.fromtimestamp(result["timestamp"][idx], timezone.utc)
        volume = quote_data.get("volume", [None])[idx]
        return Quote(
            symbol=symbol.upper(),
            price=price,
            previous_close=previous_close,
            open=_maybe_float(quote_data.get("open", [None])[idx]),
            high=_maybe_float(quote_data.get("high", [None])[idx]),
            low=_maybe_float(quote_data.get("low", [None])[idx]),
            volume=int(volume) if volume is not None else None,
            currency=meta.get("currency", "USD"),
            timestamp=ts,
        )

    def get_news(self, symbol: str, limit: int = 5) -> list[NewsItem]:
        # Public Yahoo news APIs change often; keep the production seam here and
        # return an empty list rather than failing quote collection.
        return []


class DemoProvider:
    """Deterministic provider for tests, dry runs, and first deployment."""

    def get_quote(self, symbol: str) -> Quote:
        seed = sum(ord(c) for c in symbol.upper())
        previous = 80 + seed % 120
        price = previous * (1 + ((seed % 13) - 6) / 100)
        return Quote(symbol.upper(), round(price, 2), float(previous), previous * 0.99, price * 1.02, price * 0.98, seed * 1000, "USD", datetime.now(timezone.utc))

    def get_news(self, symbol: str, limit: int = 5) -> list[NewsItem]:
        headlines = [
            ("盈利预期上修，机构关注度提升", 0.35),
            ("行业监管与宏观利率仍是主要不确定性", -0.15),
            ("盘前成交活跃，资金等待财报指引", 0.1),
        ]
        return [
            NewsItem(symbol.upper(), f"{symbol.upper()} {title}", "demo", "https://example.com", datetime.now(timezone.utc), sentiment)
            for title, sentiment in headlines[:limit]
        ]


def _maybe_float(value: object) -> float | None:
    return float(value) if value is not None else None


def build_provider(name: str) -> MarketDataProvider:
    if name == "yahoo":
        return YahooChartProvider()
    if name == "demo":
        return DemoProvider()
    raise ValueError(f"unsupported provider: {name}")
