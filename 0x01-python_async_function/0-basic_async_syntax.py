#!/usr/bin/env python3
""" an asynchronous coroutine """
import random
import asyncio


async def wait_random(max_delay=10):
    """waits for a random delay between 0 and max_delay"""
    randWait = random.uniform(0, max_delay)
    await asyncio.sleep(randWait)
    return randWait
