import pandas as pd
import numpy as np
from pandas.api.types import *
from operator_module.utils import save_dict


def main():
    data_df = pd.read_csv("../../data/favorite_purchase_predict/raw_data/train.csv")
    column_names = list(data_df.columns)
    features_names = []
    for name in column_names:
        col = data_df[name]
        if is_integer_dtype(col.dtype) or is_int64_dtype(col.dtype):
            cmax, cmin = np.max(col), np.min(col)
            if True or cmax - cmin < 33:
                r = dict(name=name, type='int')
            else:
                g = int((cmax - cmin) / 33)
                r = dict(name=name, type='int', command='group', group_dists=(g,))

        elif is_float_dtype(col.dtype):
            cmax, cmin = np.max(col), np.min(col)
            if True or cmax - cmin < 33:
                r = dict(name=name, type='float')
            else:
                g = int((cmax - cmin) / 33)
                r = dict(name=name, type='float', command='group', group_dists=(g,))

        elif is_string_dtype(col.dtype):
            r = dict(name=name, map=True)

        features_names.append(r)
    save_dict("../../data/favorite_purchase_predict/auto_features_names.json", features_names)


if __name__ == "__main__":
    main()
