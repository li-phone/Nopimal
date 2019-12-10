import numpy as np
import pandas as pd
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


def chunk2df(chunk_path, mode):
    dataset_df = pd.DataFrame()
    for m in mode:
        chunk_paths = glob.glob(os.path.join(chunk_path, r"{}_feature_*.h5".format(m)))
        for idx, chunk_path in tqdm(enumerate(chunk_paths)):
            hfs = pd.HDFStore(chunk_path)
            feature_df = hfs['feature_df']
            hfs.close()
            dataset_df = pd.concat([dataset_df, feature_df])
    return dataset_df


def main():
    # 预先定义环境
    dataset_cfg = import_module("cfg.py")
    cfg = import_module(dataset_cfg.dataset_cfg_path)
    save_dir = os.path.join(cfg.work_dirs, cfg.dataset_name)
    mkdirs(save_dir)

    test_dataset = chunk2df(cfg.split_chunk_path, mode=['test'])
    normed_test_data = norm_df(test_dataset)

    model = joblib.load(os.path.join(save_dir, "*.m"))
    pred_target = model.predict(test_dataset)

    submit_df = pd.DataFrame(

    )
    submit_df.to_csv(os.path.join(save_dir, 'infer_{}.csv'.format(get_date_str())), index=False, header=True)
    print('infer successfully!')


if __name__ == "__main__":
    main()
