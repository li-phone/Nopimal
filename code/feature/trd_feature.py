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


def main(DATA_DIR, csv_name, train=True):
    train_trd = pd.read_csv(DATA_DIR + csv_name)

    # trade_df
    # train_trd_ids = train_trd['id'].unique()
    # 提取用户历史净收入, 基本月薪, 最近一月大额消费, 历史违约次数, 历史守约次数, 违约率
    trd_kvs = {}
    for i in tqdm(range(len(train_trd))):
        row = dict(train_trd.iloc[i])
        id = row['id']
        if id not in trd_kvs:
            trd_kvs[id] = []
        trd_kvs[id].append(row)
        # if i == 100: break
    trd_features = []
    for k, v in tqdm(trd_kvs.items()):
        # keep_df = train_trd.groupby('id').get_group(id)
        keep_df = json_normalize(v)
        # bad_cnt = np.sum(keep_df['flag'])
        # good_cnt = len(keep_df) - np.sum(keep_df['flag'])
        trd_features.append(dict(
            id=k,
            salary=np.max(keep_df['cny_trx_amt']),
            recent_large_consume=np.min(keep_df['cny_trx_amt']),
            income=np.sum(keep_df['cny_trx_amt']),
            # bad_cnt=bad_cnt,
            # good_cnt=good_cnt,
            # break_rate=bad_cnt / (bad_cnt + good_cnt),
        ))
    trd_features = pd.json_normalize(trd_features)
    trd_features.to_csv(DATA_DIR + 'feature/{}_feature.csv'.format(csv_name[:-4]), index=False, header=True)


if __name__ == '__main__':
    DATA_DIR = '../../work_dirs/zsbank/data/'
    # main(DATA_DIR,'train_trd.csv')
    main(DATA_DIR, 'test_trd.csv')
