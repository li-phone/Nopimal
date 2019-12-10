# MIT License
#
# Copyright(c) [2019] [liphone/lifeng] [email: 974122407@qq.com]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this softwareand associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and /or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions :
#
# The above copyright noticeand this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import importlib
import os
import json
import numpy as np
import math
import sys
import pandas as pd
import datetime
import time


def import_module(path):
    _module = path.replace('\\', '/')
    _module = _module.split('/')
    _module[-1] = _module[-1].split('.')[0]
    _module_path = '.'.join(x for x in _module)
    return importlib.import_module(_module_path)


def mkdirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.int32):
            return int(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


def save_dict(fname, d):
    # 持久化写入
    with open(fname, "w") as fp:
        # json.dump(d, fp, cls=NpEncoder, indent=1, separators=(',', ': '))
        json.dump(d, fp, cls=NpEncoder)


def load_dict(fname):
    with open(fname, "r") as fp:
        o = json.load(fp, )
        return o


def map_col(col):
    d = {}
    for i, x in enumerate(col):
        if isinstance(x, np.int32):
            x = int(x)
        elif isinstance(x, np.float):
            x = float(x)
        elif isinstance(x, np.int64):
            x = int(x)
        if x != x:
            x = np.nan
        if x in d:
            d[x]['number'] += 1
            d[x]['index'].append(i)
        else:
            d[x] = dict(number=1, index=[i])
    return d


def dict_where(d, k, x={}, op=None):
    if k not in d:
        d[k] = x
    if op is not None:
        if op == "+=":
            d[k] += x
        elif op == "-=":
            d[k] -= x
        elif op == "*=":
            d[k] *= x
        elif op == "/=":
            d[k] /= x
    return d


class Evaluations:

    def __init__(self, names):
        self.evaluates = {name: dict(val=0, avg=0, sum=0, cnt=0) for name in names}
        head = "\n"
        for k, v in self.evaluates.items():
            head += k + "\t"
        print(head)

    def update(self, k, v):
        self.evaluates[k]['val'] = v
        self.evaluates[k]['cnt'] += 1
        self.evaluates[k]['sum'] += v
        self.evaluates[k]['avg'] = self.evaluates[k]['sum'] / self.evaluates[k]['cnt']

    def summary(self):
        c = "\n"
        for k, v in self.evaluates.items():
            c += "{:.3f}s({:.3f}s)\t".format(v['val'], v['avg'])
        print(c)


def get_date_str():
    time_str = time.strftime("%Y-%m-%d_%H%M%S", time.localtime())
    return time_str
