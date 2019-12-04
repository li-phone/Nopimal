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
from utils import *


def gen_feature_dict(raw_df, feature_names, raw_idx_df, feature_dict):
    # 统计分析特征
    target_name = feature_names[0]['name']
    targets = np.array(raw_df[target_name])
    target_uniques = np.unique(targets)
    target_uniques = np.sort(target_uniques)
    for r in feature_names:
        if r['name'] == target_name or ('operator' in r and r['operator'] != 'group'):
            continue
        c_name = r['name']
        feature_dict = dict_where(feature_dict, c_name, {})
        col = np.array(raw_df[c_name])
        c_idx = np.array(raw_idx_df[c_name])

        col = [str(x).lower() if c_idx[i] else x for i, x in enumerate(col)]
        col = np.array(col)
        col_unique = np.unique(col)
        # 去掉重复的nan值
        # col_unique = np.array(col_unique)
        # col_unique = np.unique(col_unique)
        for x in col_unique:
            if isinstance(x, np.float):
                x = float(x)
            elif isinstance(x, np.int32):
                x = int(x)
            elif isinstance(x, np.int64):
                x = int(x)
            feature_dict[c_name] = dict_where(feature_dict[c_name], x, {})
            x_index = np.where(col == x)[0]
            feature_dict[c_name][x] = dict_where(feature_dict[c_name][x], 'category_num', x_index.shape[0])
            feature_dict[c_name][x] = dict_where(feature_dict[c_name][x], 'label_num',
                                                 [0] * target_uniques.shape[0])
            target = targets[x_index]
            sum = 0
            for t in target_uniques:
                t_index = np.where(target == t)
                t_num = t_index[0].shape[0]
                sum += t_num
                feature_dict[c_name][x]['label_num'][t] += t_num
            category_num = x_index.shape[0]
            assert sum == category_num

    click_nums = np.where(targets == 1)
    click_nums = click_nums[0].shape[0]
    total_nums = targets.shape[0]
    return feature_dict, total_nums, click_nums


def draw_feature(feature_dict, img_save_dir, style='darkgrid'):
    for col_k, col_v in feature_dict.items():
        xs = col_v['label']
        y1 = col_v['category_rate']
        y2 = col_v['click_probability']
        y3 = col_v['click_rate']

        if len(xs) > 25:
            print("{} unique size is {}, more than 25".format(col_k, len(xs)))
            continue

        save_name = os.path.join(img_save_dir, "{}_bar.svg".format(col_k))
        if os.path.exists(save_name):
            continue

        sns.set(style=style)
        f, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(9, 3 * 3), sharex=True)
        x_str = [str(_) for _ in xs]
        sns.barplot(x=x_str, y=y1, palette="deep", ax=ax1)
        sns.barplot(x=x_str, y=y2, palette="deep", ax=ax2)
        sns.barplot(x=x_str, y=y3, palette="deep", ax=ax3)
        ax1.set_ylabel("category_rate")
        ax2.set_ylabel("click_probability")
        ax3.set_ylabel("click_rate")
        ax3.set_xlabel(col_k)

        plt.savefig(save_name)
        plt.show()

    # 绘制点击概率和点击比例, 点击概率和分布比例, 点击比例和分布比例的关系
    for col_k, col_v in feature_dict.items():

        col_df = pd.DataFrame(
            data={
                'label': [str(_) for _ in col_v['label']],
                'click_prob': col_v['click_probability'],
                'category_rate': col_v['category_rate'],
                'click_rate': col_v['click_rate'],
            }
        )
        sns.set(style=style)
        # f, ax = plt.subplots(figsize=(7,7))
        if len(col_v['label']) < 25:
            sns.relplot(x="category_rate", y="click_rate", size="click_prob",
                        # sizes=(40, 400),
                        alpha=.5,
                        height=7,
                        data=col_df)
            save_name = os.path.join(img_save_dir, "{}_scatter.svg".format(col_k))
            if os.path.exists(save_name):
                continue
            plt.savefig(save_name)
            plt.show()
        for x, y in zip(['category_rate', 'category_rate', 'click_rate'],
                        ['click_prob', 'click_rate', 'click_prob']):
            save_name = os.path.join(img_save_dir, "{}_{}_{}_joint.svg".format(col_k, x, y))
            if os.path.exists(save_name):
                continue
            sns.jointplot(x=x, y=y, data=col_df, kind="reg", stat_func=sci.pearsonr, xlim=(0, 1.0), ylim=(0, 1.0),
                          height=7)
            plt.savefig(save_name)
            plt.show()


def main():
    # 预先定义环境
    dataset_cfg = import_module("cfg.py")
    cfg = import_module(dataset_cfg.dataset_cfg_path)
    mkdirs(cfg.feature_save_dir)
    mkdirs(cfg.img_save_dir)

    if os.path.exists(cfg.feature_dict_file):
        feature_dict = load_dict(cfg.feature_dict_file)
    else:
        feature_dict = dict(
            success=False,
            index=0,
            total_num=0,
            total_click_num=0,
            raw_data={},
            data={},
        )

    chunk_paths = glob.glob(cfg.train_chunk_path + r"train_chunk_*.h5")
    for idx, chunk_path in tqdm(enumerate(chunk_paths)):
        if idx < feature_dict['index']:
            continue
        features_names = cfg.raw_train_file['features_names']
        for other_file in cfg.other_train_files:
            features_names.extend(other_file['features_names'])

        hfs = pd.HDFStore(chunk_path)
        raw_df, raw_idx_df = hfs['raw_df'], hfs['raw_idx_df']
        hfs.close()
        raw_df, features_names, raw_idx_df = operator(raw_df, features_names, raw_idx_df)
        features_names = [r for r in features_names if 'operator' not in r or r['operator'] == 'group']

        save_name = os.path.join(cfg.train_chunk_path, "{}_operator_chunk_{:06d}.h5".format('train', idx))
        keep_names = [r['name'] for r in features_names if 'operator' not in r or r['operator'] == 'group']
        raw_df = raw_df[keep_names]
        hfs = pd.HDFStore(save_name, complevel=6)
        hfs['operator_df'] = raw_df  # write to HDF5
        hfs.close()

        raw_dict, target_num, click_nums = gen_feature_dict(raw_df, features_names, raw_idx_df,
                                                            feature_dict['raw_data'])
        feature_dict['index'] = idx
        feature_dict['total_num'] += target_num
        feature_dict['total_click_num'] += click_nums
        feature_dict['raw_data'] = raw_dict
        save_dict(cfg.feature_dict_file, feature_dict)

    for col_k, col_v in feature_dict['raw_data'].items():
        xs = [k for k, v in col_v.items()]
        y1 = [float(v['category_num'] / max(feature_dict['total_num'], 1.)) for k, v in col_v.items()]
        y2 = [float(v['label_num'][1] / max(v['category_num'], 1.)) for k, v in col_v.items()]
        y3 = [float(v['label_num'][1] / max(feature_dict['total_click_num'], 1.)) for k, v in col_v.items()]
        feature_dict['data'][col_k] = dict(
            label=xs,
            category_rate=y1,
            click_probability=y2,
            click_rate=y3,
        )

    feature_dict['success'] = True
    save_dict(cfg.feature_dict_file, feature_dict)

    # 绘制分布直方图, 点击概率直方图, 点击比例直方图
    if cfg.draw_feature:
        draw_feature(feature_dict['data'], cfg.img_save_dir, cfg.style)

    print('generate feature dictionary successfully!')


if __name__ == "__main__":
    main()
