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


import pandas as pd
from tqdm import tqdm
import os
from operator_module.py_operator import *
from operator_module.utils import *


def split_chunk(raw_files, other_train_files, save_dir, mode='train'):
    # 批处理超大文件, 分割成chunk, 训练或测试文件
    reader = pd.read_csv(raw_files['file_path'], iterator=True, chunksize=raw_files['chunk_size'])
    chunk_cnt = 0
    for raw_df in tqdm(reader):
        save_name = os.path.join(save_dir, "{}_chunk_{:06d}.h5".format(mode, chunk_cnt))
        chunk_cnt += 1
        if os.path.exists(save_name):
            continue

        # 添加其他文件特征
        features_names = raw_files['features_names']
        raw_shape = raw_df.shape
        for other_file in other_train_files:
            features_names.extend(other_file['features_names'])
            other_df = pd.read_csv(other_file['file_path'])
            # 去掉重复的列, 保留最后一个
            other_df = other_df.drop_duplicates(subset=[other_file['primary_key']], keep=other_file['keep'])
            raw_df = pd.merge(raw_df, other_df, how='left', on=other_file['primary_key'])
            assert raw_shape[0] == raw_df.shape[0]

        raw_df = format_df(raw_df, features_names)

        hfs = pd.HDFStore(save_name, complevel=6)
        hfs['raw_df'] = raw_df  # write to HDF5
        hfs.close()


def main():
    # 预先定义环境
    dataset_cfg = import_module("cfg.py")
    cfg = import_module(dataset_cfg.dataset_cfg_path)
    mkdirs(cfg.train_chunk_path)
    mkdirs(cfg.test_chunk_path)

    split_chunk(cfg.raw_train_file, cfg.other_train_files, cfg.train_chunk_path, mode='train')
    split_chunk(cfg.raw_test_file, cfg.other_train_files, cfg.test_chunk_path, mode='test')
    print('split to chunks successfully!')


if __name__ == "__main__":
    main()
