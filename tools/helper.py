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

def invoke_print(response):
    GRAY = "\033[90m"
    RESET = "\033[0m"
    content_blocks = response.content_blocks
    for content_block in content_blocks:
        if content_block.get("type") == "reasoning":
            reasoning_content = content_block.get("reasoning")
            print(f"{GRAY}推理过程🧠：\n{reasoning_content}\n{RESET}")
        elif content_block.get("type") == "text":
            answer_content = content_block.get("text")
            print(f"正式回答💬：\n{answer_content}")
        else:
            print("出现未知类型！")
            print(content_block)

async def astream_print_with_reasoning(chunks):
    """
    异步版本的流式打印，支持 reasoning 内容显示
    与 helper.py 中的同步版功能完全一致，只是用 async for 替代 for
    """
    GRAY = "\033[90m"
    RESET = "\033[0m"
    had_reasoning = False
    full_content = []
    async for chunk in chunks:
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
            full_content.append(content)
    print()
    return "".join(full_content)