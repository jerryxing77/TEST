from __future__ import annotations

from stock_analyzer.cli import run as run_cli


def ask_choice(prompt: str, choices: dict[str, tuple[str, list[str]]]) -> list[str]:
    print(prompt)
    for key, (label, _) in choices.items():
        print(f"  {key}. {label}")
    while True:
        selected = input("请输入数字后回车：").strip()
        if selected in choices:
            return choices[selected][1]
        print("输入不正确，请重新输入。")


def main() -> int:
    print("股票信息收集分析系统 - 简单操作版")
    print("=" * 32)
    print("如果你只是想先看看效果，所有问题都选 1 即可。\n")

    session_args = ask_choice(
        "你想生成哪种报告？",
        {
            "1": ("盘前报告：开盘前看今天需要关注什么", ["--session", "premarket"]),
            "2": ("收盘报告：收盘后复盘今天发生了什么", ["--session", "close"]),
        },
    )
    provider_args = ask_choice(
        "你想使用哪种数据？",
        {
            "1": ("演示数据：不用联网，适合第一次试用", ["--provider", "demo"]),
            "2": ("Yahoo 行情：尝试获取真实行情，需要联网", ["--provider", "yahoo"]),
        },
    )

    print("\n开始生成报告，请稍等...\n")
    exit_code = run_cli(session_args + provider_args)
    print("\n完成。请打开上面 report= 后面的文件查看报告。")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
