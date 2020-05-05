import numpy as np
import pandas as pd
import os
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
from utils import *


class Config(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class Inference(object):
    def __init__(self, cfg, **kwargs):
        if isinstance(cfg, str):
            cfg = import_module(cfg)
        self.cfg = Config(**cfg.Inference)
        mkdirs(self.cfg.submit_dir)
        self.models = {}
        self.fine_models = {}

    # 2: 特征归一化
    def normalize(self, df):
        if self.cfg.normalize_type == 'StandardScaler':
            std = StandardScaler()
            return std.fit_transform(df)

    # 0: run
    def run(self):
        x1 = pd.read_csv(self.cfg.test['file'])
        test_ids = np.array(x1[self.cfg.test['uid_key']])
        x1.pop(self.cfg.test['uid_key'])
        x1 = x1.fillna(0)
        if self.cfg.normalize_type:
            x1 = self.normalize(x1)
        for v in self.cfg.models:
            model_path = os.path.join(self.cfg.model_dir, "{}.m".format(v['name']))
            checkpoint = joblib.load(model_path)
            model = checkpoint['model']
            pred_y1 = model.predict_proba(x1)
            pred_y1 = pred_y1[:, 1]
            submit_df = pd.DataFrame(
                data={
                    self.cfg.test['uid_key']: test_ids,
                    self.cfg.test['target_key']: pred_y1
                }
            )
            save_name = os.path.join(self.cfg.submit_dir, '{}_submit.txt'.format(v['name']))
            submit_df.to_csv(save_name, header=False, index=False, sep='\t')
        print('infer successfully!')


def main():
    infer = Inference('configs/zsbank.py')
    infer.run()


if __name__ == "__main__":
    main()
