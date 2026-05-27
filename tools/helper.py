import sys

def stream_print_with_reasoning(chunks):
    GRAY = "\033[90m"
    RESET = "\033[0m"
    sys.stdout.reconfigure(encoding="utf-8")
    had_reasoning = False
    full_content = []
    for chunk in chunks:
        reasoning = chunk.additional_kwargs.get("reasoning_content", "") if isinstance(chunk.additional_kwargs,dict) else ""
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
            full_content.append(content)
    print()
    return "".join(full_content)


def stream_print(chunks):
    full_content = []
    for chunk in chunks:
        content = chunk.content or ""
        if content:
            sys.stdout.write(content)
            sys.stdout.flush()
            full_content.append(content)
    print()
    return "".join(full_content)