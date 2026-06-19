from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass(frozen=True)
class Quote:
    symbol: str
    price: float
    previous_close: float
    open: float | None
    high: float | None
    low: float | None
    volume: int | None
    currency: str
    timestamp: datetime

    @property
    def change_percent(self) -> float:
        if self.previous_close == 0:
            return 0.0
        return (self.price - self.previous_close) / self.previous_close * 100

    def to_dict(self) -> dict:
        result = asdict(self)
        result["timestamp"] = self.timestamp.isoformat()
        result["change_percent"] = round(self.change_percent, 4)
        return result


@dataclass(frozen=True)
class NewsItem:
    symbol: str
    title: str
    source: str
    url: str
    published_at: datetime
    sentiment: float

    def to_dict(self) -> dict:
        result = asdict(self)
        result["published_at"] = self.published_at.isoformat()
        return result
