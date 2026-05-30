"""
@Author  : Jsy
@Date    : 2026/5/3010:44
@Description : 与时间相关的工具
"""
import time
import functools

def spent_time_async(func):
    """
        :description: 装饰器
        :param func:
        :return: 异步func所花费的时间戳
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} 本次花费的时间为：{end-start}s")
        return result
    return wrapper

def spent_time(func):
    """
    :description: 装饰器
    :param func:
    :return: func所花费的时间戳
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} 本次花费的时间为：{end-start}s",)
        return result
    return wrapper