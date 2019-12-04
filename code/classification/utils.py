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


def import_module(path):
    _module = path.replace('\\', '/')
    _module = _module.split('/')
    _module[-1] = _module[-1].split('.')[0]
    _module_path = '.'.join(x for x in _module)
    return importlib.import_module(_module_path)


def mkdirs(path):
    if not os.path.exists(path):
        os.makedirs(path)




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
        json.dump(d, fp, cls=NpEncoder, indent=1, separators=(',', ': '))


def load_dict(fname):
    with open(fname, "r") as fp:
        o = json.load(fp, )
        return o

