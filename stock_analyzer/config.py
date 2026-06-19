from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    market: str
    timezone: str
    symbols: list[str]
    benchmarks: list[str]
    risk_free_rate: float = 0.04
    report_language: str = "zh-CN"


def load_config(path: str | Path) -> AppConfig:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    symbols = [s.strip().upper() for s in data.get("symbols", []) if s.strip()]
    benchmarks = [s.strip().upper() for s in data.get("benchmarks", []) if s.strip()]
    if not symbols:
        raise ValueError("config.watchlist symbols cannot be empty")
    return AppConfig(
        market=data.get("market", "US"),
        timezone=data.get("timezone", "America/New_York"),
        symbols=symbols,
        benchmarks=benchmarks,
        risk_free_rate=float(data.get("risk_free_rate", 0.04)),
        report_language=data.get("report_language", "zh-CN"),
    )
