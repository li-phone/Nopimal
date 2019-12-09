# global settings
data_root = "../../data/video_click_predict/"
feature_save_dir = data_root + "/features/"
img_save_dir = data_root + "/imgs/"

# chunk settings
train_chunk_path = data_root + 'chunk/train/'
test_chunk_path = data_root + 'chunk/test/'
raw_train_file = dict(
    file_path=data_root + 'raw_data/train.csv',
    chunk_size=200000,
    features_names=[
        dict(name='target', type='int'),  # default str
        dict(name='pos', type='int'),
        dict(name='deviceid'),
        dict(name='app_version'),
        dict(name='newsid', type='int'),
        dict(name='device_vendor', type='str', transform='lower'),
        dict(name='netmodel', type='str', transform='lower'),
        dict(name='osversion', type='str', transform='lower'),
        dict(name='device_version', type='str', transform='lower'),
        dict(name='lng', type='float', command='group', group_dists=(10,)),
        dict(name='lat', type='float', command='group', group_dists=(10,)),
        dict(name='ts', type='int', unit=1 / 1000, command='timestamp',
             operators=('sec', 'min', 'hour', 'mday', 'mon', 'year', 'wday'))
    ]
)
raw_test_file = dict(
    file_path=data_root + 'raw_data/test.csv',
    chunk_size=200000,
    features_names=[
        dict(name='pos', type='int'),
        dict(name='deviceid'),
        dict(name='app_version'),
        dict(name='newsid', type='int'),
        dict(name='device_vendor', type='str', transform='lower'),
        dict(name='netmodel', type='str', transform='lower'),
        dict(name='osversion', type='str', transform='lower'),
        dict(name='device_version', type='str', transform='lower'),
        dict(name='ts', type='int', unit=1 / 1000, command='timestamp',
             operators=('sec', 'min', 'hour', 'mday', 'mon', 'year', 'wday'))
        # command命令用来求取特征, 非command命令只是做一些变换, 并没有用来求取特征
    ]
)
other_train_files = [
    dict(
        file_path=data_root + 'raw_data/app.csv',
        primary_key='deviceid',
        keep='last',
        features_names=[
            dict(name='applist', command='split', operators=('len',), group_dists=(10,), splits=(' ',), index=(1, -2)),
            # 长度组距为负数，则不分组
        ]
    ),
    dict(
        file_path=data_root + 'raw_data/user.csv',
        primary_key='deviceid',
        keep='last',
        features_names=[
            dict(name='outertag', command='split', operators=('len', 'sum', 'mean', 'min', 'max'),
                 group_dists=(2, 1, 0.2, 1, 1), splits=('|', ':'), ),
            dict(name='tag', command='split', operators=('len', 'sum', 'mean', 'min', 'max',),
                 group_dists=(2, 10, 2, 1, 10), splits=('|', ':'), ),
            dict(name='personidentification'),
            dict(name='gender'),
            dict(name='level', type='float', command='group', group_dists=(5,)),
            dict(name='followscore', type='float', command='group', group_dists=(2,)),
            dict(name='personalscore', type='float', command='group', group_dists=(2,)),
        ]
    )
]

# features settings
feature_dict_file = feature_save_dir + "feature_dict.json"
draw_feature = True
style = 'darkgrid'

# train settings
work_dirs = "./work_dirs/"
dataset_name = "video_click_predict"
random_state = 666
train_val_test_ratio = (0.6, 0.2, 0.2)
train_models = [
    dict(name='ABT', random_state=random_state, params=None),
    dict(name='DT', random_state=random_state, params=None),
    dict(name='GBT', random_state=random_state, params=None),
    dict(name='KNN', random_state=random_state, params=None),
    dict(name='LR', random_state=random_state, params=None),
    dict(name='GNB', random_state=random_state, params=None),
    dict(name='RF', random_state=random_state, params=None),
    dict(name='SVM', random_state=random_state, params=None),
    dict(name='XGB', random_state=random_state, params=None),
    dict(name='ET', random_state=random_state, params=None),
]


