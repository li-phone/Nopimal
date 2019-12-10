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


def get_model(name, random_state=666):
    if name == 'ABT':
        return AdaBoostClassifier(random_state=random_state)

    elif name == 'DT':
        return DecisionTreeClassifier(random_state=random_state)

    elif name == 'GBT':
        return GradientBoostingClassifier(random_state=random_state)

    elif name == 'KNN':
        return KNeighborsClassifier()

    elif name == 'LR':
        return LogisticRegression(random_state=random_state)

    elif name == 'GNB':
        return naive_bayes.GaussianNB()

    elif name == 'RF':
        return RandomForestClassifier(random_state=random_state)

    elif name == 'SVM':
        return svm.SVC(probability=True, random_state=random_state)

    elif name == 'XGB':
        return XGBClassifier(random_state=random_state)

    elif name == 'ET':
        return ExtraTreeClassifier(random_state=random_state)


def train(x, y, name, save_name=None, random_state=None):
    model = get_model(name=name, random_state=random_state)
    model.fit(x, y)  # 训练模型
    if save_name:
        joblib.dump(model, save_name, compress=5)
    return model


def evaluate(model, x, y_true, target_names=None, output_dict=False):
    y_pred = model.predict(x)
    target_names = target_names
    rpt = classification_report(y_true, y_pred, target_names=target_names, output_dict=output_dict)
    return rpt


def chunk2df(chunk_path, mode):
    dataset_df = pd.DataFrame()
    for m in mode:
        mode_dir = os.path.join(chunk_path, m)
        chunk_paths = glob.glob(os.path.join(mode_dir, r"{}_feature_chunk_*.h5".format(m)))
        for idx, chunk_path in enumerate(chunk_paths):
            hfs = pd.HDFStore(chunk_path)
            feature_df = hfs['feature_df']
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
    mkdirs(save_dir)

    train_dataset = chunk2df(cfg.split_chunk_path, mode=cfg.train_mode)
    if cfg.balanced_data:
        train_1 = train_dataset[train_dataset[cfg.target_name] == 1]
        train_0 = train_dataset.drop(train_1.index)
        rate = train_0.shape[0] / train_1.shape[0]
        if rate > 1:
            train_0 = train_0.sample(train_1.shape[0])
        elif rate < 1:
            train_1 = train_1.sample(train_0.shape[0])
        train_dataset = pd.concat([train_0, train_1])
        train_dataset = shuffle(train_dataset)

    train_labels = train_dataset.pop(cfg.target_name)

    normal_stats = None
    if cfg.normalization == 'none':
        normed_train_data = train_dataset
        normed_train_data = normed_train_data.fillna(0)
    else:
        if cfg.normalization == 'global':
            normal_mode = cfg.train_mode
            normal_mode.extend(cfg.val_mode)
            normal_stats = get_train_stats(cfg.split_chunk_path, mode=normal_mode)
        elif cfg.normalization == 'local':
            normal_stats = None
        normed_train_data = norm_df(train_dataset, normal_stats)
        normed_train_data = normed_train_data.fillna(0)

    log_df = []
    for train_model in tqdm(cfg.train_models):
        save_name = os.path.join(save_dir, "{}.m".format(train_model['name']))
        model = train(normed_train_data, train_labels, train_model['name'], save_name, train_model['random_state'])
        print('\n\n{} {} {}'.format('=' * 36, train_model['name'], '=' * 36))
        rpt_row = [train_model['name']]
        for mode in cfg.val_mode:
            val_dataset = chunk2df(cfg.split_chunk_path, mode=[mode])
            val_labels = val_dataset.pop(cfg.target_name)
            if cfg.normalization == 'none':
                normed_val_data = val_dataset
                normed_val_data = normed_val_data.fillna(0)
            else:
                normed_val_data = norm_df(val_dataset, normal_stats)
                normed_val_data = normed_val_data.fillna(0)

            print('\t{}:\n'.format(mode))
            rpt = evaluate(model, normed_val_data, val_labels, output_dict=True)
            print(evaluate(model, normed_val_data, val_labels, output_dict=False))
            rpt_row.extend([rpt['macro avg']['f1-score']])
        log_df.append(np.array(rpt_row))
    header = ['name']
    header.extend(cfg.val_mode)
    log_df = pd.DataFrame(data=np.array(log_df), columns=header)
    log_df.to_csv(os.path.join(save_dir, 'train_log.csv'), header=True)
    print('train successfully!')


if __name__ == "__main__":
    main()
