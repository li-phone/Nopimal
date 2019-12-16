# global settings
data_root = "../../data/tencent_social_ads/"
feature_save_dir = data_root + "features/"
img_save_dir = data_root + "imgs/"

# split chunk settings
split_chunk_path = data_root + 'chunk/'
raw_train_file = dict(
    file_path=data_root + 'raw_data/train.csv',
    size=3749528,
    split_mode=['train', 'valA', 'valB'],
    split_ratio=[0.6, 0.2, 0.2],
    chunk_size=200000,
    features_names=[
        dict(name='label', type='int'),
        dict(name='clickTime', type='int', map=""),
        dict(name='connectionType', type='int', map="probability"),
        dict(name='telecomsOperator', type='int', transform='lower', map="probability"),
        # negative group_dists not to carry group
    ]
)
raw_test_file = dict(
    file_path=data_root + 'raw_data/test.csv',
    size=338489,
    split_mode=['test'],
    split_ratio=[1.0],
    chunk_size=200000,
    features_names=[
        dict(name='clickTime', type='int', map=""),
        dict(name='connectionType', type='int', map="probability"),
        dict(name='telecomsOperator', type='int', transform='lower', map="probability"),
        # negative group_dists not to carry group
    ]
)
other_train_files = [
    dict(
        file_path=data_root + 'raw_data/ad.csv',
        primary_key='creativeID',
        keep='last',
        features_names=[
            dict(name='appID', type='int', map="probability"),
            dict(name='appPlatform', type='int', map="probability"),
        ]
    ),
    dict(
        file_path=data_root + 'raw_data/user.csv',
        primary_key='userID',
        keep='last',
        features_names=[
            dict(name='age', type='int', map=""),
            dict(name='gender', type='int', map="probability"),
            dict(name='education', type='int', map="probability"),
            dict(name='marriageStatus', type='int', map="probability"),
            dict(name='haveBaby', type='int', map="probability"),
            dict(name='hometown', type='int', map="probability"),
            dict(name='residence', type='int', map="probability"),
        ]
    ),
    dict(
        file_path=data_root + 'raw_data/position.csv',
        primary_key='positionID',
        keep='last',
        features_names=[
            dict(name='sitesetID', type='int', map="probability"),
            dict(name='positionType', type='int', map="probability"),
        ]
    ),
    dict(
        file_path=data_root + 'raw_data/app_categories.csv',
        primary_key='appID',
        keep='last',
        features_names=[
            dict(name='appCategory', type='int', map="probability"),
        ]
    ),
    dict(
        file_path=data_root + 'raw_data/user_app_actions_transform.csv',
        primary_key='userID',
        keep='last',
        features_names=[
            dict(name='appInstallTime', map='probability', command='split',
                 operators=('len', 'min', 'max', 'mean', 'sum'), group_dists=(-5, -5, -5, -5, -5),
                 splits=('|', ':')),
        ]
    ),
    dict(
        file_path=data_root + 'raw_data/user_installedapps_transform.csv',
        primary_key='userID',
        keep='last',
        features_names=[
            dict(name='applist', map='probability', command='split', operators=('len',), group_dists=(-5,),
                 splits=('|')),
        ]
    ),
]

# features settings
feature_mode = ['train']
target_name = 'label'
id_name = 'instanceID'
feature_dict_file = feature_save_dir + "feature_dict_train.json"
draw_feature = True
style = 'darkgrid'

# train settings
work_dirs = "./work_dirs/"
dataset_name = "tencent_social_ads"
balanced_data = True
normalization = 'none'  # global, local, none
random_state = 666
train_mode = ['train']
val_mode = ['valA', 'valB']
train_models = [
    dict(name='ABT', random_state=random_state, params=None),
    dict(name='RF', random_state=random_state, params=None),
    dict(name='XGB', random_state=random_state, params=None),
    dict(name='GBT', random_state=random_state, params=None),
    dict(name='LGB', random_state=random_state, params=None),
    dict(name='DT', random_state=random_state, params=None),
    dict(name='LR', random_state=random_state, params=None),
    dict(name='GNB', random_state=random_state, params=None),
    dict(name='ET', random_state=random_state, params=None),
    # # dict(name='KNN', random_state=random_state, params=None),
    # # dict(name='SVM', random_state=random_state, params=None),
]
