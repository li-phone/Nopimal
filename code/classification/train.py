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
from operator_module.utils import *


def norm_df(x):
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


def evaluate(model, x, y_true, target_names=None):
    y_pred = model.predict(x)
    target_names = target_names
    rpt = classification_report(y_true, y_pred, target_names=target_names, output_dict=False)
    return rpt


def main():
    # 预先定义环境
    dataset_cfg = import_module("cfg.py")
    cfg = import_module(dataset_cfg.dataset_cfg_path)
    mkdirs(os.path.join(cfg.work_dirs, cfg.dataset_name))
    from sklearn.datasets import load_iris
    # 加载数据集
    iris = load_iris()
    dataset_df = pd.DataFrame(
        data={
            'target': iris.target,
            'A': iris.data[:, 0],
            'B': iris.data[:, 1],
            'C': iris.data[:, 2],
            'D': iris.data[:, 3],
        }
    )
    # chunk_paths = glob.glob(cfg.train_chunk_path + r"train_features_*.h5")
    # for idx, chunk_path in tqdm(enumerate(chunk_paths)):
    #     hfs = pd.HDFStore(chunk_path)
    #     raw_df = hfs['raw_df']
    #     hfs.close()
    #     dataset_df = pd.concat([dataset_df, raw_df])

    train_ratio = cfg.train_val_test_ratio[0] / np.sum(cfg.train_val_test_ratio)
    train_dataset = dataset_df.sample(frac=train_ratio, random_state=cfg.random_state)
    val_test_dataset = dataset_df.drop(train_dataset.index)

    val_ratio = cfg.train_val_test_ratio[1] / np.sum(cfg.train_val_test_ratio[1:])
    val_dataset = val_test_dataset.sample(frac=val_ratio, random_state=cfg.random_state)
    test_dataset = val_test_dataset.drop(val_dataset.index)

    train_labels = train_dataset.pop('target')
    val_labels = val_dataset.pop('target')
    test_labels = test_dataset.pop('target')

    normed_train_data = norm_df(train_dataset)
    normed_val_data = norm_df(val_dataset)
    normed_test_data = norm_df(test_dataset)

    for train_model in tqdm(cfg.train_models):
        save_name = os.path.join(cfg.work_dirs, cfg.dataset_name, "{}.m".format(train_model['name']))
        model = train(normed_train_data, train_labels, train_model['name'], save_name, train_model['random_state'])
        print('\n\n' + '=' * 32 + " val " + train_model['name'] + '=' * 32)
        print(evaluate(model, normed_val_data, val_labels))
        print('\n\n' + '=' * 32 + " test " + train_model['name'] + '=' * 32)
        print(evaluate(model, normed_test_data, test_labels))


if __name__ == "__main__":
    main()
