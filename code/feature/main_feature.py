import pandas as pd
import seaborn as sn
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from pandas.api.types import is_string_dtype, is_numeric_dtype, is_float_dtype, is_int64_dtype
import matplotlib as mpl
from pandas import json_normalize
from tqdm import tqdm
import warnings

warnings.filterwarnings('ignore')

mpl.rcParams['font.sans-serif'] = ['KaiTi']
mpl.rcParams['font.serif'] = ['KaiTi']
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题,或者转换负号为字符串


def calcWOE(dataset, col, targe):
    subdata = pd.DataFrame(dataset.groupby(col)[col].count())
    suby = pd.DataFrame(dataset.groupby(col)[targe].sum())
    data = pd.DataFrame(pd.merge(subdata, suby, how="left", left_index=True, right_index=True))
    b_total = data[targe].sum()
    total = data[col].sum()
    g_total = total - b_total
    data["bad"] = data.apply(lambda x: round(x[targe] / b_total, 3), axis=1)
    data["good"] = data.apply(lambda x: round((x[col] - x[targe]) / g_total, 3), axis=1)
    data["WOE"] = data.apply(lambda x: np.log(x.bad / x.good), axis=1)
    return data.loc[:, ["bad", "good", "WOE"]]


def calcIV(dataset):
    dataset["IV"] = dataset.apply(lambda x: (x.bad - x.good) * x.WOE, axis=1)
    IV = sum(dataset["IV"])
    return IV


# 1: 查看新老用户
def analysis_new_ids(train_df, test_df, id_k='id', label_k='flag'):
    if isinstance(train_df, str):
        train_df = pd.read_csv(train_df)
    if isinstance(test_df, str):
        test_df = pd.read_csv(test_df)

    # 统计正负样本比例
    if label_k in list(train_df.columns):
        p_cnt = len(train_df[train_df[label_k] == 1])
        n_cnt = len(train_df[train_df[label_k] == 0])
        print('train set: Pos / Neg = {}'.format(p_cnt / n_cnt))

    # 统计测试集新用户和老用户
    test_ids = list(np.unique(test_df[id_k]))
    train_ids = list(np.unique(train_df[id_k]))
    old_ids = set(train_ids) & set(test_ids)
    new_ids = set(test_ids) - old_ids
    print('new_ids = {}, old_ids = {}'.format(len(new_ids), len(old_ids)))

    # 统计训练集id重复度
    train_rp_rate = len(train_ids) / len(train_df[id_k])
    print('train_rp_rate = {}'.format(1 - train_rp_rate))

    # 统计测试集id重复度
    test_rp_rate = len(test_ids) / len(test_df[id_k])
    print('test_rp_rate = {}'.format(1 - test_rp_rate))


# 2: 删除无关特征
def drop_ind_feature(data):
    drop_list = []
    for i in data.columns:
        count = data[i].count()
        if len(list(data[i].unique())) in [1, count, count - 1]:
            drop_list.append(i)
    print(drop_list)
    data.drop(drop_list, axis=1, inplace=True)
    return data


# 3: 删除缺失特征
def drop_null_feature(data):
    # 分析数值型数据缺失情况
    for type in ['number', 'object']:
        data_num = data.select_dtypes(type).copy()
        data_num_miss_rate = 1 - (data_num.count() / len(data_num))
        data_num_miss_rate.sort_values(ascending=False, inplace=True)
        miss_kv = dict(data_num_miss_rate)
        chose_cnt = -1
        print(data_num_miss_rate[:])
        data_num_miss_rate.plot()

        fig, ax1 = plt.subplots(figsize=(10, 6))
        sns.barplot(list(range(1, len(miss_kv) + 1)), data_num_miss_rate[:].values, ax=ax1)
        ax1.set_title('特征缺失情况')
        ax1.set_xlabel('缺失特征排名')
        ax1.set_ylabel('缺失占比')
        plt.show()
        for k, v in miss_kv.items():
            if v > 0.5:
                data.pop(k)
    return data


# 4: 填充缺失特征
def fill_null_feature(data):
    # 数据处理
    data_str = data.select_dtypes(exclude='number').copy()
    data_str.describe()
    for i in data_str.columns:
        data[i].fillna(data[i].mode()[0], inplace=True)

    data_num = data.select_dtypes(include='number').copy()
    data_num.describe()
    for i in data_num.columns:
        data[i].fillna(np.median(data[i]), inplace=True)

    return data


# 5: 映射字符串特征
def map_feature(data):
    data_str = data.select_dtypes(exclude='number').copy()
    for i in data_str.columns:
        col = list(data[i])
        uids = np.sort(np.unique(col))
        if len(uids) >= 20:
            print('type', i, 'value', uids)
        m = {k: i + 1 for i, k in enumerate(uids)}
        data[i] = data[i].map(m)
    return data


def process_type(df, k_v):
    for k, v in k_v.items():
        if v == 'int':
            df = df[k].astype(np.int)
        elif v == 'float':
            df = df[k].astype(np.float)
        elif v == 'str':
            df = df[k].astype(np.str)
        else:
            raise Exception('No such {} type'.format(v))
    return df


def iv_feature(df, target_key='flag', bin_num=10, min_num=20):
    columns = list(df.columns)
    columns.remove(target_key)
    iv_keys = []
    for i in columns:
        if len(df[i].unique()) > min_num:
            df[i] = pd.cut(df[i], bins=bin_num, labels=list(range(bin_num)))
        data_WOE = calcWOE(df, i, target_key)
        data_WOE['WOE'].fillna(0, inplace=True)
        data_WOE["WOE"] = data_WOE["WOE"].apply(lambda x: 0 if x == np.inf else x)
        # print(data_WOE)
        data_IV = calcIV(data_WOE)
        iv_keys.append(dict(key=i, iv=data_IV))
    iv_keys = json_normalize(iv_keys)
    iv_keys = iv_keys.sort_values('iv', ascending=False)
    iv_keys = iv_keys[iv_keys['iv'] > 0.005]
    iv_keys = iv_keys[iv_keys['iv'] != np.inf]
    print('iv_key', str(iv_keys))
    iv_keys = list(iv_keys['key'])
    # iv_keys.append(target_key)
    return iv_keys


def make_feature(df, train=True):
    # 2: 删除无关特征
    df = drop_ind_feature(df)
    # 了解数据整体情况
    print(df.info())
    # 3: 删除缺失特征
    df = drop_null_feature(df)
    # 4: 填充缺失特征
    df = fill_null_feature(df)
    # 5: 映射字符串特征
    df = map_feature(df)
    return df


if __name__ == '__main__':
    DATA_DIR = '../../work_dirs/zsbank/data/'

    train_tag = pd.read_csv(DATA_DIR + 'train_tag.csv')
    train_trd_features = pd.read_csv(DATA_DIR + 'feature/train_trd_feature.csv')
    test_tag = pd.read_csv(DATA_DIR + 'test_tag.csv')
    test_trd_features = pd.read_csv(DATA_DIR + 'feature/test_trd_feature.csv')

    # 1: 查看新老用户
    analysis_new_ids(train_tag, test_tag)
    analysis_new_ids(train_tag, train_trd_features)

    # 合并特征
    train_tag = pd.merge(train_tag, train_trd_features, on='id', how='left')
    test_tag = pd.merge(test_tag, test_trd_features, on='id', how='left')

    # 0: 读取数据
    train_tag.drop_duplicates(inplace=True)

    # 生成训练集特征
    train_tag.pop('id')
    train_labels = train_tag.pop('flag')
    train_feature = make_feature(train_tag)
    train_feature['flag'] = train_labels

    # 1: 提取IV值特征
    # iv_keys = iv_feature(train_feature)
    # train_feature = train_feature[iv_keys]
    train_feature['flag'] = train_labels

    train_feature.to_csv(DATA_DIR + 'feature/train_feature.csv', index=False)
    # 生成测试集特征
    test_ids = test_tag.pop('id')
    test_feature = make_feature(test_tag)
    # test_feature = test_feature[iv_keys]
    test_feature['id'] = test_ids
    test_feature.to_csv(DATA_DIR + 'feature/test_feature.csv', index=False)

    # type_k_v = {
    #     'job_year': 'int',
    #     # 'frs_agn_dt_cnt': 'int', 'fin_rsk_ases_grd_cd': 'int',
    #     # 'confirm_rsk_ases_lvl_typ_cd': 'int',
    # }
    # train_tag = process_type(train_tag, type_k_v)
    # test_tag = process_type(test_tag, type_k_v)

# tag_corr = train_tag.corr()
#
# # %%
# str_names = {
#     'cur_debit_crd_lvl': '招行借记卡持卡最高等级代码',
#     # 'hld_crd_card_grd_cd': '招行信用卡持卡最高等级代码',
#     'crd_card_act_ind': '信用卡活跃标识',
#     'l1y_crd_card_csm_amt_dlm_cd': '最近一年信用卡消费金额分层',
#     'atdd_type': '信用卡还款方式',
#     'perm_crd_lmt_cd': '信用卡永久信用额度分层',
#     'gdr_cd': '性别',
#     'mrg_situ_cd': '婚姻',
#     'edu_deg_cd': '教育程度',
#     'acdm_deg_cd': '学历',
#     'deg_cd': '学位',
#     'ic_ind': '工商标识',
#     'fr_or_sh_ind': '法人或股东标识',
#     # 'dnl_mbl_bnk_ind': '下载并登录招行APP标识',
#     'dnl_bind_cmb_lif_ind': '下载并绑定掌上生活标识',
#     'hav_car_grp_ind': '有车一族标识',
#     'hav_hou_grp_ind': '有房一族标识',
#     'l6mon_agn_ind': '近6个月代发工资标识',
#     # 'vld_rsk_ases_ind': '有效投资风险评估标识',
#     # 'fin_rsk_ases_grd_cd': '用户理财风险承受能力等级代码',
#     # 'confirm_rsk_ases_lvl_typ_cd': '投资强风评等级类型代码',
#     # 'cust_inv_rsk_endu_lvl_cd': '用户投资风险承受级别',
#     'l6mon_daim_aum_cd': '近6个月月日均AUM分层',
#     'tot_ast_lvl_cd': '总资产级别代码',
#     'pot_ast_lvl_cd': '潜力资产等级代码',
#     'bk1_cur_year_mon_avg_agn_amt_cd': '本年月均代发金额分层',
#     'loan_act_ind': '贷款用户标识',
#     'pl_crd_lmt_cd': '个贷授信总额度分层',
# }
# train_feature['flag'] = train_tag['flag']
# for k, v in str_names.items():
#     data = train_feature[['flag', k]]
#     ax = sns.barplot(x=k, y="flag", data=data)
#     plt.title(v)
#     plt.show()

# %%
# for x_name in list(train_tag.columns):
#     data = train_tag[['flag', x_name]]
#     ax = sns.scatterplot(x=x_name, y="flag", data=train_tag)
#     plt.show()
