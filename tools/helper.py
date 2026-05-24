import sys

def stream_print(chunks):
    # ANSI 颜色码
    GRAY = "\033[90m"
    RESET = "\033[0m"
    # 更美观的输出，区分推理过程和正式回答内容
    sys.stdout.reconfigure(encoding="utf-8")
    had_reasoning = False
    for chunk in chunks:
        reasoning = chunk.additional_kwargs.get("reasoning_content", "") if isinstance(chunk.additional_kwargs, dict) else ""
        content = chunk.content or ""
        if reasoning:
            had_reasoning = True
            sys.stdout.write(f"{GRAY}{reasoning}{RESET}")
            sys.stdout.flush()
        if content:
            if had_reasoning:
                sys.stdout.write(f"\n\n{GRAY}── 回答 ──{RESET}\n")
                sys.stdout.flush()
                had_reasoning = False
            sys.stdout.write(content)
            sys.stdout.flush()
    print()