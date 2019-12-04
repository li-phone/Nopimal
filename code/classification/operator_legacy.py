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


def is_nan(x):
    if isinstance(x, float) and (x is np.NaN or x is np.nan or np.isnan(x) or math.isnan(x)):
        return True
    elif isinstance(x, str) and len(x) == 3 and str(x).lower() == "nan":
        return True
    else:
        return False


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


def split_groups(col, group_dist=-1, c_idx=None):
    if group_dist <= 0:
        return col
    if c_idx is None:
        #     千万级别以上数据量计算速度慢, 共用索引是为了加速计算
        c_idx = [True if is_nan(_) else False for _ in col]
    assert c_idx is not None

    col_not_nan = [x for i, x in enumerate(col) if not c_idx[i]]
    if len(col_not_nan) == 0:
        return col

    # 如果为0
    grp_dist = sys.float_info.max if group_dist == 0 else group_dist
    col = [x if c_idx[i] else int(x // grp_dist) for i, x in enumerate(col)]
    return col


def operator(raw_df, feature_names, raw_idx_df=None):
    if raw_idx_df is None:
        raw_idx_df = pd.DataFrame()

    for r in feature_names:
        # 千万级别以上数据量计算速度慢, 共用索引是为了加速计算
        col = np.array(raw_df[r['name']])
        if raw_idx_df is None:
            c_idx = [True if is_nan(_) else False for _ in col]
            raw_idx_df[r['name']] = c_idx
        else:
            c_idx = raw_idx_df[r['name']]

        if 'operator' in r:
            if r['operator'] == 'group':
                new_col = split_groups(col, r['group_dist'], c_idx)
                raw_df[r['name']] = np.array(new_col)

            elif r['operator'] == 'timestamp':
                # 转换时间特征, 分别为小时和周几
                ts = np.array(col)
                if r['unit'] == 'ms':
                    ts = ts / 1000
                ts = [x if c_idx[i] else datetime.datetime.fromtimestamp(x) for i, x in enumerate(ts)]
                hour = [x if c_idx[i] else x.hour for i, x in enumerate(ts)]
                week = [x if c_idx[i] else x.weekday() for i, x in enumerate(ts)]
                raw_df[r['name'] + "_hour"] = hour
                raw_df[r['name'] + "_week"] = week
                raw_idx_df[r['name'] + "_hour"] = c_idx
                raw_idx_df[r['name'] + "_week"] = c_idx
                feature_names.append(dict(name=r['name'] + "_hour"))
                feature_names.append(dict(name=r['name'] + "_week"))

            elif r['operator'] == 'len':
                split, index = r['split'], r['index']
                s, e = index[0], index[1]
                # new_col = [x[s:e] if not is_nan(x) else x for x in col]
                # new_col = [x.split(split) if not is_nan(x) else x for x in new_col]
                # new_col = [len(x) if not is_nan(x) else x for x in new_col]
                # 一次完成更加节省时间和空间
                new_col = [x if c_idx[i] else len(x[s:e].split(split)) for i, x in enumerate(col)]
                new_col = split_groups(new_col, r['group_dist'], c_idx)
                raw_df[r['name'] + "_num"] = np.array(new_col)
                raw_idx_df[r['name'] + "_num"] = np.array(c_idx)
                feature_names.append(dict(name=r['name'] + "_num"))

            elif r['operator'] == 'len_sum_avg':
                split = r['split']
                new_col = [x if c_idx[i] else x.split(split[0]) for i, x in enumerate(col)]
                new_col_num = [x if c_idx[i] else len(x) for i, x in enumerate(new_col)]
                new_col_num = split_groups(new_col_num, r['group_dist'][0], c_idx)
                raw_df[r['name'] + "_num"] = np.array(new_col_num)
                raw_idx_df[r['name'] + "_num"] = np.array(c_idx)
                feature_names.append(dict(name=r['name'] + "_num"))

                # 平均画像得分和总得分
                new_col_float = [x if c_idx[i] else [_.split(split[1]) for _ in x] for i, x in enumerate(new_col)]
                new_col_float = [x if c_idx[i] else [float(_[1]) if len(_) >= 2 else 0 for _ in x] for i, x in
                                 enumerate(new_col_float)]
                new_c_sum = [x if c_idx[i] else np.sum(x) for i, x in enumerate(new_col_float)]
                new_c_sum = split_groups(new_c_sum, r['group_dist'][1], c_idx)
                raw_df[r['name'] + "_sum"] = np.array(new_c_sum)
                raw_idx_df[r['name'] + "_sum"] = np.array(c_idx)
                feature_names.append(dict(name=r['name'] + "_sum"))

                new_c_mean = [x if c_idx[i] else np.mean(x) for i, x in enumerate(new_col_float)]
                new_c_mean = split_groups(new_c_mean, r['group_dist'][2], c_idx)
                raw_df[r['name'] + "_mean"] = np.array(new_c_mean)
                raw_idx_df[r['name'] + "_mean"] = np.array(c_idx)
                feature_names.append(dict(name=r['name'] + "_mean"))
    return raw_df, feature_names, raw_idx_df
