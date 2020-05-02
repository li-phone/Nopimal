import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
import sklearn
from sklearn import naive_bayes
import xgboost
from numpy import loadtxt
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import *
from sklearn.tree import *
from sklearn.neighbors import *
from sklearn.linear_model import *
from sklearn import naive_bayes
from sklearn import svm  # svm支持向量机
from xgboost import *
from sklearn.utils import shuffle
from sklearn.model_selection import GridSearchCV, KFold, train_test_split
from sklearn.metrics import make_scorer, accuracy_score
import glob
import os
from tqdm import tqdm
from sklearn.externals import joblib
from sklearn.metrics.classification import *
from sklearn.metrics.regression import *
from sklearn.utils import shuffle
import lightgbm as lgb
from operator_module.utils import *


def norm_df(x, train_stats=None):
    if train_stats is None:
        train_stats = x.describe()
        train_stats = train_stats.transpose()
    return (x - train_stats['mean']) / train_stats['std']


def get_classifier_model(name, random_state=666, params=dict()):
    if name == 'ABT':
        return AdaBoostClassifier(random_state=random_state, **params)

    elif name == 'DT':
        return DecisionTreeClassifier(random_state=random_state, **params)

    elif name == 'GBT':
        return GradientBoostingClassifier(random_state=random_state, **params)

    elif name == 'KNN':
        return KNeighborsClassifier()

    elif name == 'LR':
        return LogisticRegression(random_state=random_state, **params)

    elif name == 'GNB':
        return naive_bayes.GaussianNB(**params)

    elif name == 'RF':
        return RandomForestClassifier(random_state=random_state, **params)

    elif name == 'SVM':
        return svm.SVC(probability=True, random_state=random_state, **params)

    elif name == 'XGB':
        return XGBClassifier(random_state=random_state, **params)

    elif name == 'ET':
        return ExtraTreeClassifier(random_state=random_state, **params)

    elif name == 'LGB':
        return lgb.LGBMClassifier()


def get_regressor_model(name, random_state=666, params=dict()):
    if name == 'ABT':
        return AdaBoostRegressor(random_state=random_state, **params)

    elif name == 'DT':
        return DecisionTreeRegressor(random_state=random_state, **params)

    elif name == 'GBT':
        return GradientBoostingRegressor(random_state=random_state, **params)

    elif name == 'KNN':
        return KNeighborsRegressor()

    elif name == 'LR':
        return LogisticRegression(random_state=random_state, **params)

    elif name == 'RF':
        return RandomForestRegressor(random_state=random_state, **params)


    elif name == 'XGB':
        return XGBRFRegressor(random_state=random_state, **params)

    elif name == 'ET':
        return ExtraTreeRegressor(random_state=random_state, **params)

    elif name == 'LGB':
        return lgb.LGBMRegressor()


def train(x, y, name, type, save_name=None, random_state=None, params=dict()):
    if type == 'Regressor':
        model = get_regressor_model(name=name, random_state=random_state, params=params)
    else:
        model = get_classifier_model(name=name, random_state=random_state, params=params)
    model.fit(x, y)  # 训练模型
    if save_name:
        joblib.dump(model, save_name, compress=5)
    return model


def evaluate(model, x, y_true, type='', output_dict=False):
    y_pred = model.predict(x)
    if type == 'Regressor':
        rpt = mean_squared_error(y_true, y_pred)
        return str(rpt)
    else:
        rpt = classification_report(y_true, y_pred, output_dict=output_dict)
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
    dataset_cfg = import_module("cfg.py")
    cfg = import_module(dataset_cfg.dataset_cfg_path)
    save_dir = os.path.join(cfg.work_dirs, cfg.dataset_name, 'mode_' + '_'.join(cfg.train_mode))
    mkdirs(save_dir)

    train_dataset = chunk2df(cfg.split_chunk_path, mode=cfg.train_mode)
    # 先求normalization参数
    normal_stats = None
    if cfg.normalization == 'global':
        normal_mode = cfg.train_mode
        normal_mode.extend(cfg.val_mode)
        normal_stats = get_train_stats(cfg.split_chunk_path, mode=normal_mode)
    elif cfg.normalization == 'local':
        normal_stats = None

    # 是否平衡数据集
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

    # 标准化
    if cfg.normalization == 'none':
        normed_train_data = train_dataset
        normed_train_data = normed_train_data.fillna(0)
    else:
        normed_train_data = norm_df(train_dataset, normal_stats)
        normed_train_data = normed_train_data.fillna(0)

    # log_df = []
    for train_model in tqdm(cfg.train_models):
        save_name = os.path.join(save_dir, "{}.m".format(train_model['name']))
        model = train(normed_train_data, train_labels, train_model['name'], cfg.train_type, save_name,
                      train_model['random_state'], train_model['params'])
        print('\n\n{} {} {}'.format('=' * 36, train_model['name'], '=' * 36))
        # rpt_row = [train_model['name']]

        val_dataset = chunk2df(cfg.split_chunk_path, mode=cfg.val_mode)
        val_labels = val_dataset.pop(cfg.target_name)
        if cfg.normalization == 'none':
            normed_val_data = val_dataset
            normed_val_data = normed_val_data.fillna(0)
        else:
            normed_val_data = norm_df(val_dataset, normal_stats)
            normed_val_data = normed_val_data.fillna(0)

        rpt_str = evaluate(model, normed_val_data, val_labels, cfg.train_type, )
        print(rpt_str)
        with open(os.path.join(save_dir, 'train_log.txt'), 'a') as fp:
            fp.write(train_model['name'] + ':\n' + rpt_str + '\n')
        # rpt = evaluate(model, normed_val_data, val_labels, output_dict=True)
        # rpt_row.extend([rpt['macro avg']['f1-score']])
        # log_df.append(np.array(rpt_row))
    # header = ['name','f1-score']
    # log_df = pd.DataFrame(data=np.array(log_df), columns=header)
    # log_df.to_csv(os.path.join(save_dir, 'train_log.csv'), header=True)
    print('train successfully!')


if __name__ == "__main__":
    main()
