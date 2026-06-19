# 股票信息收集分析系统

这是一套轻量级股票信息收集与分析系统，用于每天盘前和收盘后自动生成观察池报告。系统默认使用可重复的 `demo` 数据源，便于部署验证；生产环境可切换到 `yahoo` 行情源，或在 `stock_analyzer/providers.py` 中接入券商、新闻或付费数据 API。

## 功能

- 维护股票观察池与基准指数配置。
- 收集价格、涨跌幅、成交量和新闻情绪。
- 生成盘前（`premarket`）和收盘（`close`）Markdown 分析报告。
- 保存原始快照 JSON，方便复盘和后续量化分析。
- 输出风险提示，例如异常波动、放量和负面新闻情绪。

## 不懂代码先看这里

如果你不熟悉命令行，先看 `使用说明.md`，然后运行：

```bash
python run.py
```

按提示选择即可；第一次试用可以所有问题都选 `1`。

## 快速开始

```bash
python -m stock_analyzer --session premarket --provider demo
python -m stock_analyzer --session close --provider demo
```

报告会写入 `reports/`，数据快照会写入 `data/`。

## 配置观察池

编辑 `config/watchlist.json`：

```json
{
  "market": "US",
  "timezone": "America/New_York",
  "symbols": ["AAPL", "MSFT", "NVDA", "SPY", "QQQ"],
  "benchmarks": ["SPY", "QQQ"],
  "risk_free_rate": 0.04,
  "report_language": "zh-CN"
}
```

## 定时任务示例

在美国东部时间交易日执行：

```cron
# 盘前 08:00 汇总
0 8 * * 1-5 cd /path/to/project && python -m stock_analyzer --session premarket --provider yahoo
# 收盘后 16:20 汇总
20 16 * * 1-5 cd /path/to/project && python -m stock_analyzer --session close --provider yahoo
```

## 扩展建议

- 在 `MarketDataProvider` 协议下增加 Alpha Vantage、Polygon、IEX Cloud、券商 API 等数据源。
- 增加邮件、飞书、Slack、企业微信推送。
- 增加财报日历、期权隐含波动率、宏观数据和板块轮动模型。
- 将 `data/*.json` 导入数据库或数据湖，构建长期表现和事件复盘面板。
