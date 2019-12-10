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
import time
import glob
from operator_module.py_operator import *
from operator_module.utils import *


def get_draw_dict(feature_dict):
    for col_k, col_v in feature_dict['raw_data'].items():
        # print('key', col_k)
        labels = [k for k, v in col_v.items()]
        labels = np.sort(labels)
        sum_0, sum_1 = 0, 0
        for label in labels:
            if '0' in col_v[label]:
                sum_0 += col_v[label]['0']
            if '1' in col_v[label]:
                sum_1 += col_v[label]['1']
        # assert sum_0 + sum_1 == feature_dict['total_num']
        category_rates, click_probabilities, click_rates = [], [], []
        for label in labels:
            num_0, num_1 = 0, 0
            if '0' in col_v[label]:
                num_0 = col_v[label]['0']
            if '1' in col_v[label]:
                num_1 = col_v[label]['1']
            num = max(num_0 + num_1, 1)
            click_probabilities.append(num_1 / num)
            click_rates.append(num_1 / max(sum_1, 1))
            category_rates.append(num / max(sum_0 + sum_1, 1))

        feature_dict['data'][col_k] = dict(
            label=labels,
            category_rate=category_rates,
            click_probability=click_probabilities,
            click_rate=click_rates,
        )
    return feature_dict


def draw_feature(feature_dict, img_save_dir, style='darkgrid'):
    for col_k, col_v in feature_dict.items():
        xs = np.array(col_v['label'])
        y1 = np.array(col_v['category_rate'])
        y2 = np.array(col_v['click_probability'])
        y3 = np.array(col_v['click_rate'])

        if len(xs) > 25:
            y2_idx = np.argsort(-y2)
            keep_idx = y2_idx[:24]
            xs = xs[keep_idx]
            y1 = y1[keep_idx]
            y2 = y2[keep_idx]
            y3 = y3[keep_idx]

        save_name = os.path.join(img_save_dir, "{}_bar.png".format(col_k))
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

    # # 绘制点击概率和点击比例, 点击概率和分布比例, 点击比例和分布比例的关系
    # for col_k, col_v in feature_dict.items():
    #
    #     col_df = pd.DataFrame(
    #         data={
    #             'label': [str(_) for _ in col_v['label']],
    #             'click_prob': col_v['click_probability'],
    #             'category_rate': col_v['category_rate'],
    #             'click_rate': col_v['click_rate'],
    #         }
    #     )
    #     sns.set(style=style)
    #     # f, ax = plt.subplots(figsize=(7,7))
    #     if len(col_v['label']) < 25:
    #         sns.relplot(x="category_rate", y="click_rate", size="click_prob",
    #                     # sizes=(40, 400),
    #                     alpha=.5,
    #                     height=7,
    #                     data=col_df)
    #         save_name = os.path.join(img_save_dir, "{}_scatter.png".format(col_k))
    #         if os.path.exists(save_name):
    #             continue
    #         plt.savefig(save_name)
    #         plt.show()
    #     for x, y in zip(['category_rate', 'category_rate', 'click_rate'],
    #                     ['click_prob', 'click_rate', 'click_prob']):
    #         save_name = os.path.join(img_save_dir, "{}_{}_{}_joint.png".format(col_k, x, y))
    #         if os.path.exists(save_name):
    #             continue
    #         sns.jointplot(x=x, y=y, data=col_df, kind="reg", stat_func=sci.pearsonr, xlim=(0, 1.0), ylim=(0, 1.0),
    #                       height=7)
    #         plt.savefig(save_name)
    #         plt.show()


def gen_dict(cfg, feature_dict):
    for mode in cfg.feature_mode:
        mode_dir = os.path.join(cfg.split_chunk_path, mode)
        chunk_paths = glob.glob(os.path.join(mode_dir, r"{}_chunk_*.h5".format(mode)))
        evaluations = Evaluations(["operator_df", "count_df"])
        if mode not in feature_dict:
            feature_dict[mode] = dict(index=-1)

        for idx, chunk_path in tqdm(enumerate(chunk_paths)):
            if idx <= feature_dict[mode]['index']:
                continue
            features_names = cfg.raw_train_file['features_names'].copy()
            for other_file in cfg.other_train_files:
                features_names.extend(other_file['features_names'])

            hfs = pd.HDFStore(chunk_path)
            raw_df = hfs['raw_df']
            hfs.close()

            stime = time.time()
            raw_df, features_names = operator_df(raw_df, features_names)
            evaluations.update("operator_df", time.time() - stime)

            save_name = os.path.join(mode_dir, "{}_operator_chunk_{:06d}.h5".format(mode, idx))
            keep_names = [r['name'] for r in features_names]
            raw_df = raw_df[keep_names]
            if not os.path.exists(save_name):
                hfs = pd.HDFStore(save_name, complevel=6)
                hfs['operator_df'] = raw_df  # write to HDF5
                hfs.close()

            stime = time.time()
            feature_dict['raw_data'] = count_df(raw_df, features_names, feature_dict['raw_data'])
            evaluations.update("count_df", time.time() - stime)

            feature_dict[mode]['index'] = idx
            feature_dict['total_num'] += raw_df.shape[0]
            save_dict(cfg.feature_dict_file, feature_dict)
            save_dict(cfg.feature_dict_file + ".bak", feature_dict)
            evaluations.summary()

    return feature_dict


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
            total_num=0,
            raw_data={},
            data={},
        )

    if feature_dict['success'] is not True:
        feature_dict = gen_dict(cfg, feature_dict)
        feature_dict['success'] = True
        save_dict(cfg.feature_dict_file, feature_dict)

    # 绘制分布直方图, 点击概率直方图, 点击比例直方图
    if cfg.draw_feature:
        d = get_draw_dict(feature_dict)
        draw_feature(d['data'], cfg.img_save_dir, cfg.style)

    print('generate feature dictionary successfully!')


if __name__ == "__main__":
    main()
