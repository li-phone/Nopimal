import numpy as np
import pandas as pd
import glob
import os
from tqdm import tqdm
from sklearn.externals import joblib
from sklearn.metrics import classification_report
from sklearn.utils import shuffle
from utils import *


def norm_df(x, train_stats=None):
    if train_stats is None:
        train_stats = x.describe()
        train_stats = train_stats.transpose()
    return (x - train_stats['mean']) / train_stats['std']


def chunk2df(chunk_path, mode, glob_word='feature_chunk', h5_key='feature_df'):
    dataset_df = pd.DataFrame()
    for m in mode:
        mode_dir = os.path.join(chunk_path, m)
        chunk_paths = glob.glob(os.path.join(mode_dir, r"{}_{}_*.h5".format(m, glob_word)))
        for idx, chunk_path in enumerate(chunk_paths):
            hfs = pd.HDFStore(chunk_path)
            feature_df = hfs[h5_key]
            hfs.close()
            dataset_df = pd.concat([dataset_df, feature_df])

    columns = np.sort(dataset_df.columns)
    dataset_df = dataset_df[list(columns)]
    return dataset_df


def get_train_stats(split_chunk_path, mode):
    x = chunk2df(split_chunk_path, mode=mode)
    train_stats = x.describe()
    train_stats = train_stats.transpose()
    return train_stats


def main():
    # 预先定义环境
    cfg = import_module("cfg.py")
    save_dir = os.path.join(cfg.work_dirs, 'submit')
    mkdirs(save_dir)

    test_dataset = pd.read_csv(cfg.test_feature)
    # 先求normalization参数
    normal_stats = None
    if cfg.normalization == 'global':
        normal_mode = cfg.train_mode
        normal_mode.extend(cfg.val_mode)
        normal_stats = get_train_stats(cfg.split_chunk_path, mode=normal_mode)
    elif cfg.normalization == 'local':
        normal_stats = None

    # 标准化
    if cfg.normalization == 'none':
        normed_test_data = test_dataset
        normed_test_data = normed_test_data.fillna(0)
    else:
        normed_test_data = norm_df(test_dataset, normal_stats)
        normed_test_data = normed_test_data.fillna(0)

    test_csv = pd.read_csv(cfg.test_csv)
    test_ids = np.array(test_csv[cfg.id_name])
    for r in tqdm(cfg.train_models):
        model_name = r['name']
        save_name = os.path.join(cfg.work_dirs + '/models', "{}.m".format(model_name))
        model = joblib.load(save_name)
        test_pred_target = model.predict_proba(normed_test_data)
        test_pred_target = test_pred_target[:, 1]
        submit_df = pd.DataFrame(
            data={
                cfg.id_name: test_ids,
                cfg.target_name: test_pred_target
            }
        )
        save_name = os.path.join(save_dir, '{}_infer_submit.txt'.format(model_name))
        submit_df.to_csv(save_name, header=False, index=False, sep='\t')
    print('infer successfully!')


if __name__ == "__main__":
    main()
