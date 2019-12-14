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
from operator_module.utils import *
from operator_module.py_operator import *


def raw2feature_df(raw_df, feature_names, feature_dict):
    for i in range(1, len(feature_names)):
        r = feature_names[i]
        name = r['name']
        col = list(raw_df[name])
        if 'map' in r and r['map'] is True:
            col = [x if isinstance(x, list) else [x] for x in col]
            col = [["$NaN$" if y != y else str(y) for y in x] for x in col]
            for j, x in enumerate(col):
                p = 0
                for y in x:
                    if y in feature_dict[name]:
                        p += feature_dict[name][y]['p']
                col[j] = p
            raw_df[name] = col
        else:
            col = [0 if x != x else x for x in col]
            raw_df[name] = col

    return raw_df


def gen_feature(raw_file, other_files, feature_dict, split_chunk_path):
    for mode in tqdm(raw_file['split_mode']):
        mode_dir = os.path.join(split_chunk_path, mode)
        chunk_paths = glob.glob(os.path.join(mode_dir, r"{}_chunk_*.h5".format(mode)))

        for idx, chunk_path in tqdm(enumerate(chunk_paths)):
            save_name = os.path.join(mode_dir, "{}_feature_chunk_{:06d}.h5".format(mode, idx))
            if os.path.exists(save_name):
                continue

            features_names = raw_file['features_names'].copy()
            for other_file in other_files:
                features_names.extend(other_file['features_names'])

            operator_path = os.path.join(mode_dir, "{}_operator_chunk_{:06d}.h5".format(mode, idx))
            if os.path.exists(operator_path):
                hfs = pd.HDFStore(operator_path)
                raw_df = hfs['operator_df']
                hfs.close()
                features_names = feature_dict['features_names']
            else:
                hfs = pd.HDFStore(chunk_path)
                raw_df = hfs['raw_df']
                hfs.close()
                raw_df, features_names = operator_df(raw_df, features_names)
                keep_names = [r['name'] for r in features_names]
                raw_df = raw_df[keep_names]

            raw_df = raw2feature_df(raw_df, features_names, feature_dict['raw_data'])
            hfs = pd.HDFStore(save_name, complevel=6)
            hfs['feature_df'] = raw_df  # write to HDF5
            hfs.close()


def main():
    # 预先定义环境
    dataset_cfg = import_module("cfg.py")
    cfg = import_module(dataset_cfg.dataset_cfg_path)
    mkdirs(cfg.feature_save_dir)

    feature_dict = load_dict(cfg.feature_dict_file)
    for col_k, col_v in feature_dict['raw_data'].items():
        for k, v in col_v.items():
            num_0, num_1 = 0, 0
            if '0' in v:
                num_0 = v['0']
            if '1' in v:
                num_1 = v['1']
            p = num_1 / max(num_0 + num_1, 1)
            v['p'] = p

    gen_feature(cfg.raw_train_file, cfg.other_train_files, feature_dict, cfg.split_chunk_path)
    gen_feature(cfg.raw_test_file, cfg.other_train_files, feature_dict, cfg.split_chunk_path)
    print('generate feature successfully!')


if __name__ == "__main__":
    main()
