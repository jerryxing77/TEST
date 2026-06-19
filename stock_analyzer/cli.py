from __future__ import annotations

import argparse

from .config import load_config
from .providers import build_provider
from .report import render_report, write_report
from .storage import save_snapshot


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="股票信息收集分析系统")
    parser.add_argument("--config", default="config/watchlist.json", help="观察池配置文件")
    parser.add_argument("--provider", default="demo", choices=["demo", "yahoo"], help="行情数据源")
    parser.add_argument("--session", default="close", choices=["premarket", "close"], help="报告场景")
    parser.add_argument("--data-dir", default="data", help="快照输出目录")
    parser.add_argument("--report-dir", default="reports", help="报告输出目录")
    args = parser.parse_args(argv)

    config = load_config(args.config)
    provider = build_provider(args.provider)
    quotes = [provider.get_quote(symbol) for symbol in config.symbols]
    news = [item for symbol in config.symbols for item in provider.get_news(symbol)]
    snapshot_path = save_snapshot(args.data_dir, args.session, quotes, news)
    report_path = write_report(args.report_dir, args.session, render_report(args.session, quotes, news))
    print(f"snapshot={snapshot_path}")
    print(f"report={report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
