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
from line_profiler import LineProfiler
from .utils import *


def col2feature(col, index, fea_attrib, labels, fea_names, fea_values):
    features = [[0] * len(fea_names) for i in range(len(fea_names))]
    fea_attribs = [dict(name=fea_attrib['name'] + "_" + x) for x in fea_names]
    for i, label in enumerate(col):
        idx = labels.index(label)
        if -1 != idx:
            for j, _ in enumerate(fea_names):
                features[j][i] = fea_values[j][i]
        else:
            index[i] = True
            print('Warning!!! No such "{}" label'.format(label))

    return features, fea_attribs


# ----------------------------------------- Split Chunks Data Frame API -----------------------------------------
# 数据初步处理，做单位转换，大小写消歧等处理
def format_col(col, r):
    if 'type' in r:
        if r['type'] == 'int':
            if 'unit' in r:
                g = r['unit']
            else:
                g = 1.
            col = [x if x != x else int(x * g) for x in col]

        elif r['type'] == 'float':
            if 'unit' in r:
                g = r['unit']
            else:
                g = 1.
            col = [x if x != x else float(x * g) for x in col]

        elif r['type'] == 'str':
            col = [x if x != x else str(x) for x in col]
            if 'transform' in r and r['transform'] == 'lower':
                col = [x.lower() for x in col]
            elif 'transform' in r and r['transform'] == 'upper':
                col = [x.upper() for x in col]

    return col


def format_df(raw_df, feature_names):
    for r in feature_names:
        raw_df[r['name']] = format_col(raw_df[r['name']], r)

    return raw_df


# ----------------------------------------- Generate Features Dictionary API -----------------------------------------
# 先生成特征集，再得到特征词典
def get_time_type(t, type):
    if "sec" == type:
        return t.second
    elif "min" == type:
        return t.minute
    elif "hour" == type:
        return t.hour
    elif "mday" == type:
        return t.day
    elif "mon" == type:
        return t.month
    elif "year" == type:
        return t.year
    elif "wday" == type:
        return t.weekday()
    return -1


def operator_col(col, fea_attrib):
    out_features, fea_attribs = [], []
    if "timestamp" == fea_attrib['command']:
        ts = [x if x != x else datetime.datetime.fromtimestamp(x) for x in col]
        for operator in fea_attrib['operators']:
            h = [x if x != x else get_time_type(x, operator) for x in ts]
            fea_attribs.append(dict(name=fea_attrib['name'] + "_" + str(operator), command="timestamp"))
            out_features.append(h)

    elif "group" == fea_attrib['command']:
        for g in fea_attrib['group_dists']:
            col = [x if x != x else int(x / g) for x in col]
        out_features.append(col)
        fea_attribs.append(fea_attrib)

    elif "split" == fea_attrib['command']:
        if 'index' in fea_attrib:
            s, e = fea_attrib['index']
            col = [x if x != x else x[s:e] for x in col]

        tags = []
        for i, split in enumerate(fea_attrib['splits']):
            if i >= 1:
                tags = [x if x != x else [_.split(split)[0] if len(_.split(split)) >= 1 else np.nan for _ in x] for x
                        in col]
                col = [x if x != x else [_.split(split)[1] if len(_.split(split)) >= 2 else '0' for _ in x] for x
                       in col]
                col = [x if x != x else [float(_) for _ in x] for x in col]
            else:
                col = [x if x != x else x.split(split) for x in col]
                tags = col

        fea_attribs.append(dict(name=fea_attrib['name'] + "_tags", command="split"))
        out_features.append(tags)

        g = fea_attrib['group_dists']
        for g_idx, operator in enumerate(fea_attrib['operators']):
            if "len" == operator:
                out_feature = [x if x != x else len(x) for x in col]
                if g[g_idx] > 0:
                    out_feature = [x if x != x else int(x / g[g_idx]) for x in out_feature]
                fea_attribs.append(dict(name=fea_attrib['name'] + "_len", command="split"))
                out_features.append(out_feature)
            elif "sum" == operator:
                if g[g_idx] > 0:
                    out_feature = [x if x != x else int(np.sum(x) / g[g_idx]) for x in col]
                else:
                    out_feature = [x if x != x else np.sum(x) for x in col]
                fea_attribs.append(dict(name=fea_attrib['name'] + "_sum", command="split"))
                out_features.append(out_feature)
            elif "mean" == operator:
                if g[g_idx] > 0:
                    out_feature = [x if x != x else int(np.mean(x) / g[g_idx]) for x in col]
                else:
                    out_feature = [x if x != x else np.mean(x) for x in col]
                fea_attribs.append(dict(name=fea_attrib['name'] + "_mean", command="split"))
                out_features.append(out_feature)
            elif "max" == operator:
                if g[g_idx] > 0:
                    out_feature = [x if x != x else int(np.max(x) / g[g_idx]) for x in col]
                else:
                    out_feature = [x if x != x else np.max(x) for x in col]
                fea_attribs.append(dict(name=fea_attrib['name'] + "_max", command="split"))
                out_features.append(out_feature)
            elif "min" == operator:
                if g[g_idx] > 0:
                    out_feature = [x if x != x else int(np.min(x) / g[g_idx]) for x in col]
                else:
                    out_feature = [x if x != x else np.min(x) for x in col]
                fea_attribs.append(dict(name=fea_attrib['name'] + "_min", command="split"))
                out_features.append(out_feature)

    return out_features, fea_attribs


# @profile
def operator_df(raw_df, features_names):
    rs = []
    for r in features_names:
        if 'command' in r:
            col = raw_df[r['name']]
            col = [np.nan if x != x else x for x in col]
            features, fea_attribs = operator_col(col, r)
            for feature, attr in zip(features, fea_attribs):
                rs.append(attr)
                raw_df[attr['name']] = feature
        else:
            rs.append(r)

    return raw_df, rs


def count_col(targets, cols, col_cnt_dict):
    for col, target in zip(cols, targets):
        for x in col:
            if x not in col_cnt_dict:
                col_cnt_dict[x] = {}
            if target not in col_cnt_dict[x]:
                col_cnt_dict[x][target] = 1
            else:
                col_cnt_dict[x][target] += 1

    return col_cnt_dict


# @profile
def count_df(raw_df, feature_names, feature_dict):
    targets = raw_df[feature_names[0]['name']]
    targets = [str(x) for x in targets]
    for i in range(1, len(feature_names)):
        r = feature_names[i]
        if r['name'] not in feature_dict:
            feature_dict[r['name']] = dict()
        col = list(raw_df[r['name']])
        col = [x if isinstance(x, list) else [x] for x in col]
        col = [["$NaN$" if y != y else str(y) for y in x] for x in col]

        feature_dict[r['name']] = count_col(targets, col, feature_dict[r['name']])

    return feature_dict
