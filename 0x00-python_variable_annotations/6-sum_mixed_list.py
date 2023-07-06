#!/usr/bin/env python3
"""type-annotated function sum_mixed_list"""
from typing import Union, List


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """type-annotated function sum_mixed_list which takes a list
    mxd_lst of integers and floats and returns their sum as a float"""
    mixed_total = 0
    for element in range(0, len(mxd_lst)):
        mixed_total += mxd_lst[element]
    return float(mixed_total)
