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


import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
import os
import numpy as np
import scipy.stats as sci
import datetime
import math
import json
from numba import jit
import sys
import glob
from cutils import *
from utils import *



def _raw2feature():
    results = []
    for raw_r in raw_np:
        rst_r = {keep_names[0]: raw_r[0]}

        for j in xrange(1, keep_names.shape[0]):
            keep_name = keep_names[j]
            label = str(raw_r[j])
            if _is_nan(label):
                label = str(label).lower()
            f = feature_dict[keep_name]
            dict_idx = f[label].index(label)
            for k in feature_keys:
                cat_rate = f[k][dict_idx]
                rst_r[str(keep_name) + "_" + k] = cat_rate
        results.append(rst_r)
    results_np = [[v for k, v in r.items()] for r in results]
    results_np = np.array(results_np)
    columns = [k for k, v in results[0].items()]
    return results_np, columns

def save_feature_df(raw_df, save_name, feature_dict):
    results = []
    for i in range(raw_df.shape[0]):
        raw_r = raw_df.iloc[i]
        rst_r = {keep_names[0]: raw_r[keep_names[0]]}

        for j in range(1, len(keep_names)):
            k = keep_names[j]
            label = str(raw_r[k])
            if is_nan(label):
                label = str(label).lower()
            f = feature_dict[k]
            dict_idx = f['label'].index(label)
            cat_rate = f['category_rate'][dict_idx]
            clk_rate = f['click_rate'][dict_idx]
            clk_prob = f['click_probability'][dict_idx]
            rst_r[str(k) + "_cat_rate"] = clk_rate
            rst_r[str(k) + "_clk_rate"] = clk_rate
            rst_r[str(k) + "_clk_prob"] = clk_prob
        results.append(rst_r)
    results_np = [[v for k, v in r.items()] for r in results]
    results_np = np.array(results_np)
    columns = [k for k, v in results[0].items()]
    feature_df = pd.DataFrame(data=results_np, columns=columns)

    hfs = pd.HDFStore(save_name, complevel=6)
    hfs['feature_df'] = feature_df  # write to HDF5
    hfs.close()


def gen_feature(chunk_paths, raw_file, other_files, feature_dict, save_dir, mode='train'):
    for idx, chunk_path in tqdm(enumerate(chunk_paths)):
        save_name = os.path.join(save_dir, "{}_feature_chunk_{:06d}.h5".format(mode, idx))
        if os.path.exists(save_name):
            continue

        features_names = raw_file['features_names'].copy()
        for other_file in other_files:
            features_names.extend(other_file['features_names'])

        operator_path = os.path.join(save_dir, "{}_operator_chunk_{:06d}.h5".format(mode, idx))
        if os.path.exists(operator_path):
            hfs = pd.HDFStore(operator_path)
            raw_df = hfs['operator_df']
            hfs.close()
        else:
            hfs = pd.HDFStore(chunk_path)
            raw_df, raw_idx_df = hfs['raw_df']
            hfs.close()
            raw_df, features_names = operator_df(raw_df, features_names)
            keep_names = [r['name'] for r in features_names]
            raw_df = raw_df[keep_names]

        save_feature_df(raw_df, save_name, feature_dict)

def main():
    # 预先定义环境
    dataset_cfg = import_module("cfg.py")
    cfg = import_module(dataset_cfg.dataset_cfg_path)
    mkdirs(cfg.feature_save_dir)

    feature_dict = load_dict(cfg.feature_dict_file)
    train_chunk_paths = glob.glob(cfg.train_chunk_path + r"train_chunk_*.h5")
    test_chunk_paths = glob.glob(cfg.test_chunk_path + r"test_chunk_*.h5")

    gen_feature(train_chunk_paths, cfg.raw_train_file, cfg.other_train_files, feature_dict['data'],
                cfg.train_chunk_path,
                mode='train')
    gen_feature(test_chunk_paths, cfg.raw_test_file, cfg.other_train_files, feature_dict['data'], cfg.test_chunk_path,
                mode='test')
    print('generate feature successfully!')


if __name__ == "__main__":
    main()
