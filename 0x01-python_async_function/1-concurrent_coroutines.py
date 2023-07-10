#!/usr/bin/env python3
"""multiple coroutines at the same time with async"""
import asyncio
wait_random = __import__('0-basic_async_syntax').wait_random


def bubble_sort(lst):
    """bubble sort to sort the list"""
    n = len(lst)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    return lst


async def wait_n(n: int, max_delay: int) -> float:
    """2 int arguments (in this order): n and max_delay
    """
    list_of_delay = []
    for i in range(n):
        delay = await wait_random(max_delay)
        list_of_delay.append(delay)
    sorted_delay_list = bubble_sort(list_of_delay)
    return sorted_delay_list
