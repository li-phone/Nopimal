import pandas as pd
import numpy as np
from tqdm import tqdm


def map_k_list(data_df, pk):
    data_dict = {}
    for i in range(data_df.shape[0]):
        row = data_df.iloc[i]
        r_id = row[pk]
        if r_id not in data_dict:
            data_dict[r_id] = []
        data_dict[r_id].append(list(row))
    return data_dict


def map2k(pk='userID', fk='applist'):
    data_df = pd.read_csv("../../../data/tencent_social_ads/raw_data/user_installedapps.csv")
    data_dict = map_k_list(data_df, pk=pk)
    data_np = []
    for k, v in tqdm(data_dict.items()):
        keep_col = [str(x[1]) for x in v]
        line = '|'.join(keep_col)
        data_np.append(np.array([k, line]))
    data_df = pd.DataFrame(data=data_np, columns=[pk, fk])
    data_df.to_csv("user_installedapps_transform.csv", index=False, header=True)


def map2kv(pk='userID', vk='appID'):
    data_df = pd.read_csv("../../../data/tencent_social_ads/raw_data/user_app_actions.csv")
    data_np = []
    data_dict = map_k_list(data_df, pk=pk)
    for k, v in tqdm(data_dict.items()):
        keep_col = ['{}:{}'.format(x[2], x[1]) for x in v]
        line = "|".join(keep_col)
        data_np.append(np.array([k, line]))
    data_df = pd.DataFrame(
        data=data_np, columns=['userID', 'appInstallTime']
    )
    data_df.to_csv("user_app_actions_transform.csv", index=False, header=True)


def main():
    map2k()
    map2kv()


if __name__ == "__main__":
    main()
