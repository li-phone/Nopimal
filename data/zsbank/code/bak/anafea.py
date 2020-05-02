import pandas as pd
import seaborn as sn
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from pandas.api.types import is_string_dtype, is_numeric_dtype, is_float_dtype, is_int64_dtype
import matplotlib as mpl

mpl.rcParams['font.sans-serif'] = ['KaiTi']
mpl.rcParams['font.serif'] = ['KaiTi']
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题,或者转换负号为字符串


def analysis_new_ids(train_df, test_df, id_k='id', label_k='flag'):
    if isinstance(train_df, str):
        train_df = pd.read_csv(train_df)
    if isinstance(test_df, str):
        test_df = pd.read_csv(test_df)

    # 统计正负样本比例
    p_cnt = len(train_df[train_df[label_k] == 1])
    n_cnt = len(train_df[train_df[label_k] == 0])
    print('train set: Pos / Neg = {}'.format(p_cnt / n_cnt))

    # 统计测试集新用户和老用户
    test_ids = np.unique(test_df[id_k])
    train_ids = np.unique(train_df[id_k])
    old_ids = set(train_ids) and set(test_ids)
    new_ids = set(test_ids) - old_ids
    print('new_ids = {}, old_ids = {}'.format(len(new_ids), len(old_ids)))

    # 统计训练集id重复度
    train_rp_rate = len(train_ids) / len(train_df[id_k])
    print('train_rp_rate = {}'.format(1 - train_rp_rate))

    # 统计测试集id重复度
    test_rp_rate = len(test_ids) / len(test_df[id_k])
    print('test_rp_rate = {}'.format(1 - test_rp_rate))


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


def process_feature(df):
    cnames = list(df.columns)
    for name in cnames:
        if is_string_dtype(df[name]):
            col = list(df[name])
            col = [_ if _ == _ else '$' for _ in col]
            uids = np.unique(col)
            uids = np.sort(uids)
            if len(uids) >= 20:
                print('type', name, 'value', uids)
            m = {k: i + 1 for i, k in enumerate(uids)}
            col = [m[k] for k in list(col)]
            df[name] = col
        elif is_float_dtype(df[name]):
            pass
        elif is_int64_dtype(df[name]):
            pass
        else:
            pass
    return df


DATA_DIR = './data/'
train_tag = pd.read_csv(DATA_DIR + 'train_tag.csv')
test_tag = pd.read_csv(DATA_DIR + 'test_tag.csv')
analysis_new_ids(train_tag, test_tag)

type_k_v = {
    # 'job_year': 'int',
    # 'frs_agn_dt_cnt': 'int', 'fin_rsk_ases_grd_cd': 'int',
    # 'confirm_rsk_ases_lvl_typ_cd': 'int',
}
train_tag = process_type(train_tag, type_k_v)
test_tag = process_type(test_tag, type_k_v)

train_names = list(train_tag.columns)
train_names.remove('id')
train_names.remove('flag')
train_feature = train_tag[train_names]
train_feature = process_feature(train_feature)
train_feature['flag'] = train_tag['flag']
train_feature.to_csv(DATA_DIR + 'train_feature.csv', index=False)

test_names = list(test_tag.columns)
test_names.remove('id')
test_feature = test_tag[test_names]
test_feature = process_feature(test_feature)
test_feature.to_csv(DATA_DIR + 'test_feature.csv', index=False)
# %%


tag_corr = train_tag.corr()

# %%
str_names = {
    'cur_debit_crd_lvl': '招行借记卡持卡最高等级代码',
    # 'hld_crd_card_grd_cd': '招行信用卡持卡最高等级代码',
    'crd_card_act_ind': '信用卡活跃标识',
    'l1y_crd_card_csm_amt_dlm_cd': '最近一年信用卡消费金额分层',
    'atdd_type': '信用卡还款方式',
    'perm_crd_lmt_cd': '信用卡永久信用额度分层',
    'gdr_cd': '性别',
    'mrg_situ_cd': '婚姻',
    'edu_deg_cd': '教育程度',
    'acdm_deg_cd': '学历',
    'deg_cd': '学位',
    'ic_ind': '工商标识',
    'fr_or_sh_ind': '法人或股东标识',
    # 'dnl_mbl_bnk_ind': '下载并登录招行APP标识',
    'dnl_bind_cmb_lif_ind': '下载并绑定掌上生活标识',
    'hav_car_grp_ind': '有车一族标识',
    'hav_hou_grp_ind': '有房一族标识',
    'l6mon_agn_ind': '近6个月代发工资标识',
    # 'vld_rsk_ases_ind': '有效投资风险评估标识',
    # 'fin_rsk_ases_grd_cd': '用户理财风险承受能力等级代码',
    # 'confirm_rsk_ases_lvl_typ_cd': '投资强风评等级类型代码',
    # 'cust_inv_rsk_endu_lvl_cd': '用户投资风险承受级别',
    'l6mon_daim_aum_cd': '近6个月月日均AUM分层',
    'tot_ast_lvl_cd': '总资产级别代码',
    'pot_ast_lvl_cd': '潜力资产等级代码',
    'bk1_cur_year_mon_avg_agn_amt_cd': '本年月均代发金额分层',
    'loan_act_ind': '贷款用户标识',
    'pl_crd_lmt_cd': '个贷授信总额度分层',
}
train_feature['flag'] = train_tag['flag']
for k, v in str_names.items():
    data = train_feature[['flag', k]]
    ax = sns.barplot(x=k, y="flag", data=data)
    plt.title(v)
    plt.show()

# %%
# for x_name in list(train_tag.columns):
#     data = train_tag[['flag', x_name]]
#     ax = sns.scatterplot(x=x_name, y="flag", data=train_tag)
#     plt.show()

# %%
