from __future__ import annotations

from datetime import datetime
from pathlib import Path

from .analysis import average_sentiment, market_breadth, rank_movers, risk_flags
from .models import NewsItem, Quote


def render_report(session: str, quotes: list[Quote], news: list[NewsItem]) -> str:
    session_name = "盘前" if session == "premarket" else "收盘"
    breadth = market_breadth(quotes)
    movers = rank_movers(quotes)[:10]
    lines = [
        f"# {session_name}股票信息汇总分析",
        "",
        f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 市场概览",
        f"- 上涨：{breadth['advancers']}，下跌：{breadth['decliners']}，平盘：{breadth['unchanged']}",
        f"- 观察池平均涨跌幅：{breadth['average_change_percent']}%",
        f"- 新闻平均情绪：{average_sentiment(news)}（-1 到 1）",
        "",
        "## 重点标的",
        "| 股票 | 最新价 | 涨跌幅 | 成交量 |",
        "| --- | ---: | ---: | ---: |",
    ]
    for q in movers:
        volume = f"{q.volume:,}" if q.volume is not None else "N/A"
        lines.append(f"| {q.symbol} | {q.price:.2f} {q.currency} | {q.change_percent:.2f}% | {volume} |")
    lines.extend(["", "## 风险提示与行动项"])
    flags = risk_flags(quotes, news)
    if flags:
        lines.extend(f"- {flag}" for flag in flags)
    else:
        lines.append("- 未发现超阈值异常；继续跟踪宏观数据、财报日程与盘前成交。")
    lines.extend(["", "## 新闻摘要"])
    if news:
        for item in news[:20]:
            lines.append(f"- [{item.symbol}] {item.title}（{item.source}，情绪 {item.sentiment:+.2f}）")
    else:
        lines.append("- 当前数据源未返回新闻；可接入付费新闻/API 源扩展。")
    lines.append("")
    return "\n".join(lines)


def write_report(report_dir: str | Path, session: str, content: str) -> Path:
    Path(report_dir).mkdir(parents=True, exist_ok=True)
    path = Path(report_dir) / f"{datetime.utcnow().strftime('%Y%m%d')}_{session}.md"
    path.write_text(content, encoding="utf-8")
    return path
