# global settings
data_root = "../../data/video_click_predict/"
feature_save_dir = data_root + "features/"
img_save_dir = data_root + "imgs/"

# split chunk settings
split_chunk_path = data_root + 'chunk/'
raw_train_file = dict(
    file_path=data_root + 'raw_data/train.csv',
    size=11376681,
    split_mode=['train', 'valA', 'valB'],
    split_ratio=[0.6, 0.2, 0.2],
    chunk_size=200000,
    features_names=[
        dict(name='target', type='int'),  # default str
        dict(name='pos', type='int', map='onehot'),
        dict(name='deviceid', map='onehot'),
        dict(name='app_version', map='onehot'),
        dict(name='newsid', type='int', map='onehot'),
        dict(name='device_vendor', type='str', transform='lower', map='onehot'),
        dict(name='netmodel', type='str', transform='lower', map='onehot'),
        dict(name='osversion', type='str', transform='lower', map='onehot'),
        dict(name='device_version', type='str', transform='lower', map='onehot'),
        dict(name='lng', type='float', command='group', group_dists=(-5,)),
        dict(name='lat', type='float', command='group', group_dists=(-5,)),
        dict(name='ts', type='int', unit=1 / 1000, command='timestamp',
             operators=('hour', 'mday', 'wday'))
        # negative group_dists not to carry group
    ]
)
raw_test_file = dict(
    file_path=data_root + 'raw_data/test.csv',
    size=3653592,
    split_mode=['test'],
    split_ratio=[1.0],
    chunk_size=200000,
    features_names=[
        dict(name='pos', type='int'),
        dict(name='deviceid', map='onehot'),
        dict(name='app_version', map='onehot'),
        dict(name='newsid', type='int', map='onehot'),
        dict(name='device_vendor', type='str', transform='lower', map='onehot'),
        dict(name='netmodel', type='str', transform='lower', map='onehot'),
        dict(name='osversion', type='str', transform='lower', map='onehot'),
        dict(name='device_version', type='str', transform='lower', map='onehot'),
        dict(name='lng', type='float', command='group', group_dists=(-5,)),
        dict(name='lat', type='float', command='group', group_dists=(-5,)),
        dict(name='ts', type='int', unit=1 / 1000, command='timestamp',
             operators=('hour', 'mday', 'wday'))
        # command命令用来求取特征, 非command命令只是做一些变换, 并没有用来求取特征
    ]
)
other_train_files = [
    dict(
        file_path=data_root + 'raw_data/app.csv',
        primary_key='deviceid',
        keep='last',
        features_names=[
            dict(name='applist', command='split', operators=('len',), group_dists=(-5,), splits=(' ',), index=(1, -2)),
            # 长度组距为负数，则不分组
        ]
    ),
    dict(
        file_path=data_root + 'raw_data/user.csv',
        primary_key='deviceid',
        keep='last',
        features_names=[
            dict(name='outertag', command='split', operators=('len', 'sum', 'mean', 'min', 'max'),
                 group_dists=(-1, -1, -0.5, -1, -1), splits=('|', ':'), ),
            dict(name='tag', command='split', operators=('len', 'sum', 'mean', 'min', 'max',),
                 group_dists=(-2, -10, -2, -1, -10), splits=('|', ':'), ),
            dict(name='personidentification', map='onehot'),
            dict(name='gender', map='onehot'),
            dict(name='level', type='float', command='group', group_dists=(-2,)),
            dict(name='followscore', type='float', command='group', group_dists=(-1,)),
            dict(name='personalscore', type='float', command='group', group_dists=(-1,)),
        ]
    )
]

# features settings
feature_mode = ['train']
target_name = 'target'
id_name = 'PassengerId'
feature_dict_file = feature_save_dir + "feature_dict_train.json"
draw_feature = True
style = 'darkgrid'

# train settings
train_type = 'Regressor'
work_dirs = "./work_dirs/"
dataset_name = "video_click_predict"
balanced_data = False
normalization = 'none'  # global, local, none
random_state = 666
train_mode = ['train']
val_mode = ['valA', 'valB']
train_models = [
    dict(name='ABT', random_state=random_state, params=dict()),
    dict(name='RF', random_state=random_state, params=dict()),
    dict(name='XGB', random_state=random_state, params=dict()),
    dict(name='GBT', random_state=random_state, params=dict()),
    dict(name='LGB', random_state=random_state, params=dict()),
    dict(name='DT', random_state=random_state, params=dict()),
    dict(name='LR', random_state=random_state, params=dict()),
    dict(name='GNB', random_state=random_state, params=dict()),
    dict(name='ET', random_state=random_state, params=dict()),
    # dict(name='SVM', random_state=random_state, params=dict()),
    # dict(name='KNN', random_state=random_state, params=None),
]
