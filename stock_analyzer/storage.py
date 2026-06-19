from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from .models import NewsItem, Quote


def save_snapshot(data_dir: str | Path, session: str, quotes: list[Quote], news: list[NewsItem]) -> Path:
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    stamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    path = Path(data_dir) / f"{stamp}_{session}.json"
    payload = {"session": session, "created_at": stamp, "quotes": [q.to_dict() for q in quotes], "news": [n.to_dict() for n in news]}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path
