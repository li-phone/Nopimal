# -*- coding:utf-8 -*-

import os, sys
import sys


def mix():
    return [1, 2, 3, 4]


def format_col():
    return ["中文", "DEF"], {"transform": "lower", "type": "str"}, [False, False]


def operator_col():
    return [1.2, 3.4], {"type": "float", "command": "group", "group_dists": (1.,)}, [False, True]


def col2feature():
    return [1.2, 3.4, 5.6], {"type": "float"}, [False, False], [1.2, 3.4], ['a', 'b'], [[1, 3], [2, 4]]


def count_col():
    return [1, 0, 1], [4.1, 5.2, 5.3], {"type": "float"}

