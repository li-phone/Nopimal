import pandas as pd
from tqdm import tqdm
import os


def split(df, rate=0.8, random_state=666, label_k='flag'):
    if isinstance(df, str):
        df = pd.read_csv(df)
    train_df = df.sample(frac=rate, random_state=random_state)
    val_df = df.drop(train_df.index)
    train_rate = len(train_df[train_df[label_k] == 1]) / len(train_df[train_df[label_k] == 0])
    val_rate = len(val_df[val_df[label_k] == 1]) / len(val_df[val_df[label_k] == 0])
    print('train: pos / neg = {}'.format(train_rate))
    print('val: pos / neg = {}'.format(val_rate))
    return train_df, val_df


def main():
    train_df, val_df = split('../work_dirs/zsbank/data/train_feature.csv')
    train_df.to_csv('../work_dirs/zsbank/data/split_train_feature.csv', index=False)
    val_df.to_csv('../work_dirs/zsbank/data/split_val_feature.csv', index=False)
    print('split train and val successfully!')


if __name__ == "__main__":
    main()
