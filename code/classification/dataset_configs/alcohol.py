# global settings
data_root = "../../data/winequality_dataset/"
feature_save_dir = data_root + "features/"
img_save_dir = data_root + "imgs/"

# split chunk settings
split_chunk_path = data_root + 'chunk/'
raw_train_file = dict(
    file_path=data_root + 'raw_data/train.csv',
    size=3397,
    split_mode=['train', 'valA', 'valB'],
    split_ratio=[0.6, 0.2, 0.2],
    chunk_size=200000,
    features_names=[
        dict(name='quality', type='int'),
        dict(name='fixed acidity', type='float'),
        dict(name='volatile acidity', type='float'),
        dict(name='citric acid', type='float'),
        dict(name='residual sugar', type='float'),
        dict(name='chlorides', type='float'),
        dict(name='free sulfur dioxide', type='float'),
        dict(name='total sulfur dioxide', type='float'),
        dict(name='density', type='float'),
        dict(name='pH', type='float'),
        dict(name='sulphates', type='float'),
        dict(name='alcohol', type='float'),
    ]
)
raw_test_file = dict(
    file_path=data_root + 'raw_data/test.csv',
    size=1500,
    split_mode=['test'],
    split_ratio=[1.0],
    chunk_size=200000,
    features_names=[
        dict(name='fixed acidity', type='float'),
        dict(name='volatile acidity', type='float'),
        dict(name='citric acid', type='float'),
        dict(name='residual sugar', type='float'),
        dict(name='chlorides', type='float'),
        dict(name='free sulfur dioxide', type='float'),
        dict(name='total sulfur dioxide', type='float'),
        dict(name='density', type='float'),
        dict(name='pH', type='float'),
        dict(name='sulphates', type='float'),
        dict(name='alcohol', type='float'),
    ]
)
other_train_files = []

# features settings
feature_mode = ['train']
target_name = 'quality'
id_name = 'id'
feature_dict_file = feature_save_dir + "feature_dict_train.json"
draw_feature = True
style = 'darkgrid'

# train settings
train_type = 'Regressor'
work_dirs = "./work_dirs/"
dataset_name = "alcohol"
balanced_data = False
normalization = 'none'  # global, local, none
random_state = 666
train_mode = ['train', 'valA', 'valB']
val_mode = ['valA', 'valB']
train_models = [
    dict(name='ABT', random_state=random_state, params=dict()),
    dict(name='RF', random_state=random_state, params=dict()),
    dict(name='XGB', random_state=random_state, params=dict()),
    dict(name='GBT', random_state=random_state, params=dict()),
    dict(name='LGB', random_state=random_state, params=dict()),
    dict(name='DT', random_state=random_state, params=dict()),
    dict(name='ET', random_state=random_state, params=dict()),
    dict(name='KNN', random_state=random_state, params=None),
    dict(name='LR', random_state=random_state, params=dict()),
    # dict(name='GNB', random_state=random_state, params=dict()),
    # dict(name='SVM', random_state=random_state, params=dict()),
]
