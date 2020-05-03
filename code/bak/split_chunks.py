import pandas as pd
from tqdm import tqdm
import os
from operator_module.py_operator import *
from operator_module.utils import *


def split_chunk(raw_files, other_train_files, save_dir):
    reader = pd.read_csv(raw_files['file_path'], iterator=True)
    for mode, ratio in tqdm(zip(raw_files['split_mode'], raw_files['split_ratio'])):
        mode_dir = os.path.join(save_dir, mode)
        mkdirs(mode_dir)

        mode_size = int(raw_files['size'] * ratio)
        chunk_cnt = 0
        while mode_size > 0:
            try:
                chunk_size = min(raw_files['chunk_size'], mode_size)
                mode_size -= chunk_size
                save_name = os.path.join(mode_dir, "{}_chunk_{:06d}.h5".format(mode, chunk_cnt))
                chunk_cnt += 1
                if os.path.exists(save_name):
                    continue

                # 添加其他文件特征
                raw_df = reader.get_chunk(chunk_size)
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

            except StopIteration:
                print("Iteration is stopped.")
                break


def main():
    # 预先定义环境
    dataset_cfg = import_module("cfg.py")
    cfg = import_module(dataset_cfg.dataset_cfg_path)

    split_chunk(cfg.raw_train_file, cfg.other_train_files, cfg.split_chunk_path)
    split_chunk(cfg.raw_test_file, cfg.other_train_files, cfg.split_chunk_path)
    print('split to chunks successfully!')


if __name__ == "__main__":
    main()
