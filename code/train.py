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
from pandas import json_normalize
from sklearn.metrics import roc_auc_score
from sklearn.metrics import classification_report
from tqdm import tqdm
from sklearn.externals import joblib
from sklearn.utils import shuffle
import lightgbm as lgb
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import roc_auc_score, roc_curve, auc
import matplotlib.pyplot as plt
from mlxtend.classifier import StackingClassifier
from utils import *

try:
    pass
except:
    pass


def norm_df(x, train_stats=None):
    if train_stats is None:
        train_stats = x.describe()
        train_stats = train_stats.transpose()
    return (x - train_stats['mean']) / train_stats['std']


def get_classifier(type, random_state=666, **params):
    if type == 'ABT':
        return AdaBoostClassifier(random_state=random_state, **params)

    elif type == 'DT':
        return DecisionTreeClassifier(random_state=random_state, **params)

    elif type == 'GBT':
        return GradientBoostingClassifier(random_state=random_state, **params)

    elif type == 'KNN':
        return KNeighborsClassifier()

    elif type == 'LR':
        return LogisticRegression(random_state=random_state, **params)

    elif type == 'GNB':
        return naive_bayes.GaussianNB(**params)

    elif type == 'RF':
        return RandomForestClassifier(random_state=random_state, **params)

    elif type == 'SVM':
        return svm.SVC(random_state=random_state, **params)

    elif type == 'XGB':
        return XGBClassifier(random_state=random_state, **params)

    elif type == 'ET':
        return ExtraTreeClassifier(random_state=random_state, **params)

    elif type == 'LGB':
        return lgb.LGBMClassifier()


def model_metrics(clf, X_train, X_test, y_train, y_test, name=None):
    y_train_pred = clf.predict(X_train)
    y_test_pred = clf.predict(X_test)
    y_train_proba = clf.predict_proba(X_train)[:, 1]
    y_test_proba = clf.predict_proba(X_test)[:, 1]

    # report = []
    # # 训练集
    # report.append('训练集: ')
    # train_rpt = classification_report(y_train, y_train_pred)
    # train_auc = roc_auc_score(y_train, y_train_proba)
    # train_auc = 'auc score = {}'.format(train_auc)
    # report.append(train_rpt)
    # report.append(train_auc)
    #
    # # 测试集
    # report.append('测试集: ')
    # test_rpt = classification_report(y_test, y_test_pred)
    # test_auc = roc_auc_score(y_test, y_test_proba)
    # test_auc = 'auc score = {}'.format(test_auc)
    # report.append(test_rpt)
    # report.append(test_auc)

    # 准确率
    rpt_df = [
        dict(
            name=name,
            mode='train',
            accuracy=accuracy_score(y_train, y_train_pred),
            precision=precision_score(y_train, y_train_pred),
            recall=recall_score(y_train, y_train_pred),
            f1_score=f1_score(y_train, y_train_pred),
            auc_score=roc_auc_score(y_train, y_train_proba)
        ),
        dict(
            name=name,
            mode='test',
            accuracy=accuracy_score(y_test, y_test_pred),
            precision=precision_score(y_test, y_test_pred),
            recall=recall_score(y_test, y_test_pred),
            f1_score=f1_score(y_test, y_test_pred),
            auc_score=roc_auc_score(y_test, y_test_proba)
        ),
    ]
    # rpt_df = json_normalize(rpt_df)
    # report.append(str(rpt_df))
    # roc曲线
    fpr_train, tpr_train, thresholds_train = roc_curve(y_train, y_train_proba, pos_label=1)
    fpr_test, tpr_test, thresholds_test = roc_curve(y_test, y_test_proba, pos_label=1)

    label = ['Train - AUC:{:.4f}'.format(auc(fpr_train, tpr_train)),
             'Test - AUC:{:.4f}'.format(auc(fpr_test, tpr_test))]
    plt.plot(fpr_train, tpr_train)
    plt.plot(fpr_test, tpr_test)
    plt.plot([0, 1], [0, 1], 'd--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend(label, loc=4)
    plt.title('{} ROC curve'.format(name))
    plt.show()
    return rpt_df


def mkdirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


def echo_log(info, log_file=None):
    if log_file is None:
        print(info)
    else:
        print(info)
        with open(log_file, 'a+') as fp:
            fp.write(info)


class Config(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class Trainer(object):
    def __init__(self, cfg, **kwargs):
        if isinstance(cfg, str):
            cfg = import_module(cfg)
        self.cfg = Config(**cfg.Trainer)
        mkdirs(self.cfg.model_dir)
        self.models = {}
        self.fine_models = {}

    # 1: 平衡数据集
    def balance(self, df):
        if self.cfg.balance_data:
            pos = df[df[self.cfg.train['target_key']] == 1]
            neg = df.drop(pos.index)
            rate = pos.shape[0] / neg.shape[0]
            if rate < 1:
                neg = neg.sample(len(pos))
            elif rate > 1:
                pos = pos.sample(len(neg))
            df = pd.concat([pos, neg])
            df = shuffle(df)
            return df

    # 2: 特征归一化
    def normalize(self, df):
        if self.cfg.normalize_type == 'StandardScaler':
            std = StandardScaler()
            return std.fit_transform(df)

    # 3: 训练数据集
    def train(self, x, y, type, name, params):
        model = get_classifier(type=type, **params)
        model.fit(x, y)  # 训练模型
        d = dict(model=model, type=type, params=params)
        self.models[name] = d
        save_name = os.path.join(self.cfg.model_dir, name + '.m')
        joblib.dump(d, save_name, compress=5)
        return model

    # 4: 模型调优
    def finetune(self, x1, y1, x2, y2, type, name, params, param_grid, cv=4):
        model = get_classifier(type=type, **params)
        gsearch = GridSearchCV(model, param_grid=param_grid, scoring='roc_auc', cv=cv)
        gsearch.fit(x1, y1)
        echo_log('\n最佳参数: {}'.format(gsearch.best_params_), self.cfg.log_file)
        echo_log('\n训练集的最佳分数：{}'.format(gsearch.best_score_), self.cfg.log_file)
        echo_log('\n测试集的最佳分数: {}'.format(gsearch.score(x2, y2)), self.cfg.log_file)

        fine_model = get_classifier(type=type, **gsearch.best_params_)
        fine_model.fit(x1, y1)
        d = dict(model=fine_model, type=type, params=gsearch.best_params_)
        self.fine_models[name] = d
        save_name = os.path.join(self.cfg.model_dir, name + '_finetune.m')
        joblib.dump(d, save_name, compress=5)
        return fine_model

    # 5: 模型融合
    def stack_models(self, x1, y1, x2, y2, meta):
        classifiers = [v['model'] for k, v in self.fine_models.items()]
        meta_classifier = self.fine_models[meta]['model']
        sclf_lr = StackingClassifier(
            classifiers=classifiers,
            meta_classifier=meta_classifier,
            use_probas=True,
            average_probas=True,
            use_features_in_secondary=True
        )
        sclf_lr.fit(x1, y1.values)
        d = dict(model=sclf_lr, name='stacking_models', meta_classifier=meta)
        save_name = os.path.join(self.cfg.model_dir, 'stacking_models.m')
        joblib.dump(d, save_name, compress=5)
        return sclf_lr

    # 0: run
    def run(self):
        x1 = pd.read_csv(self.cfg.train['file'])
        x2 = pd.read_csv(self.cfg.val['file'])
        x1 = x1.fillna(0)
        x2 = x2.fillna(0)
        y1 = x1.pop(self.cfg.train['target_key'])
        y2 = x2.pop(self.cfg.val['target_key'])
        if self.cfg.balance_data:
            x1 = self.balance(x1)
        if self.cfg.normalize_type:
            x1 = self.normalize(x1)
            x2 = self.normalize(x2)
        train_results = []
        for v in self.cfg.models:
            self.train(x1, y1, v['type'], v['name'], v['params'])
            train_results.extend(model_metrics(self.models[v['name']]['model'], x1, x2, y1, y2, v['name']))
            self.finetune(
                x1, y1, x2, y2, v['type'], v['name'], v['params'], v['param_grid'])
            train_results.extend(
                model_metrics(self.fine_models[v['name']]['model'], x1, x2, y1, y2, 'fine_' + v['name']))

        stack_model = self.stack_models(x1, y1, x2, y2, self.cfg.stack_meta)
        train_results.extend(model_metrics(stack_model, x1, x2, y1, y2, 'stack_' + v['name']))
        train_results = json_normalize(train_results)
        train_results.sort_values(by=['mode', 'auc_score'], ascending=False)
        echo_log(str(train_results), self.cfg.log_file)


def main():
    trainer = Trainer('configs/zsbank.py')
    trainer.run()
    print('train successfully!')


if __name__ == "__main__":
    main()
