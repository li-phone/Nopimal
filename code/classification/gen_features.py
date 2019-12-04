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




def gen_feature(chunk_paths, raw_file, other_files, feature_dict, save_dir, mode='train'):
    for idx, chunk_path in tqdm(enumerate(chunk_paths)):
        save_name = os.path.join(save_dir, "{}_feature_chunk_{:06d}.h5".format(mode, idx))
        # if os.path.exists(save_name):
        #     continue

        features_names = raw_file['features_names']
        for other_file in other_files:
            features_names.extend(other_file['features_names'])
        operator_path = os.path.join(save_dir, "{}_operator_chunk_{:06d}.h5".format(mode, idx))
        if os.path.exists(operator_path):
            hfs = pd.HDFStore(operator_path)
            raw_df = hfs['operator_df']
            hfs.close()
        else:
            hfs = pd.HDFStore(chunk_path)
            raw_df, raw_idx_df = hfs['raw_df'].head(2000), hfs['raw_idx_df'].head(2000)
            hfs.close()
            raw_df, features_names, raw_idx_df = operator(raw_df, features_names, raw_idx_df)
        keep_names = [r['name'] for r in features_names if 'operator' not in r or r['operator'] == 'group']
        raw_df = raw_df[keep_names]
        save_feature_df(raw_df, keep_names, save_name, feature_dict)


def main():
    # 预先定义环境
    dataset_cfg = import_module("cfg.py")
    cfg = import_module(dataset_cfg.dataset_cfg_path)
    mkdirs(cfg.feature_save_dir)

    # feature_dict = load_dict(cfg.feature_dict_file)
    feature_dict = load_dict("feature_dict_debug.json")
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
