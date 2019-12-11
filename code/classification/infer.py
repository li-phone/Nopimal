import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
import sklearn
from sklearn import naive_bayes
import xgboost
from numpy import loadtxt
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import naive_bayes
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm  # svm支持向量机
from xgboost import XGBClassifier
from sklearn.tree import ExtraTreeClassifier
from sklearn.utils import shuffle
from sklearn.model_selection import GridSearchCV, KFold, train_test_split
from sklearn.metrics import make_scorer, accuracy_score
import glob
import os
from tqdm import tqdm
from sklearn.externals import joblib
from sklearn.metrics import classification_report
from sklearn.utils import shuffle
from operator_module.utils import *


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

    return dataset_df


def get_train_stats(split_chunk_path, mode):
    x = chunk2df(split_chunk_path, mode=mode)
    train_stats = x.describe()
    train_stats = train_stats.transpose()
    return train_stats


def main():
    # 预先定义环境
    dataset_cfg = import_module("cfg.py")
    cfg = import_module(dataset_cfg.dataset_cfg_path)
    save_dir = os.path.join(cfg.work_dirs, cfg.dataset_name)
    submit_dir = os.path.join(save_dir, "submit")
    mkdirs(submit_dir)
    mkdirs(save_dir)

    test_dataset = chunk2df(cfg.split_chunk_path, mode=cfg.raw_test_file['split_mode'])
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

    raw_test_df = chunk2df(cfg.split_chunk_path, cfg.raw_test_file['split_mode'], 'chunk', 'raw_df')
    raw_test_ids = np.array(raw_test_df['id'])
    for r in tqdm(cfg.train_models):
        model_name = r['name']
        save_name = os.path.join(save_dir, "{}.m".format(model_name))
        model = joblib.load(save_name)
        test_pred_target = model.predict(normed_test_data)
        submit_df = pd.DataFrame(
            data=dict(
                id=raw_test_ids,
                target=test_pred_target
            )
        )
        save_name = os.path.join(submit_dir, '{}_infer_submit.csv'.format(model_name))
        submit_df.to_csv(save_name, header=True, index=False)

    submit_df = None
    model_names = ['ABT', 'RF', 'XGB', 'LR', 'DT', 'ET','GBT','GNB']
    for model_name in model_names:
        save_name = os.path.join(submit_dir, '{}_infer_submit.csv'.format(model_name))
        m_df = pd.read_csv(save_name)
        if submit_df is None:
            submit_df = m_df
        else:
            submit_df['target'] += m_df['target']
    col = list(submit_df['target'])
    col = [1 if x >= (len(model_names) + 0) // 2 else 0 for x in col]
    submit_df['target'] = col
    save_name = os.path.join(submit_dir, '{}_vote_submit.csv'.format('_'.join(model_names)))
    submit_df.to_csv(save_name, header=True, index=False)

    print('infer successfully!')


if __name__ == "__main__":
    main()
