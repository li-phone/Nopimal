# global settings
data_root = "../../data/titanic/"
feature_save_dir = data_root + "features/"
img_save_dir = data_root + "imgs/"

# split chunk settings
split_chunk_path = data_root + 'chunk/'
raw_train_file = dict(
    file_path=data_root + 'raw_data/train.csv',
    size=891,
    split_mode=['train', 'valA', 'valB'],
    split_ratio=[0.6, 0.2, 0.2],
    chunk_size=200000,
    features_names=[
        dict(name='Survived', type='int'),
        dict(name='Pclass', type='int', map=True),
        dict(name='Sex', map=True),
        dict(name='Age', type='int', map=False),
        dict(name='SibSp', type='int', map=False),
        dict(name='Parch', type='int', map=False),
        dict(name='Fare', type='float'),
        dict(name='Cabin', map=True),
        dict(name='Embarked', map=True),
    ]
)
raw_test_file = dict(
    file_path=data_root + 'raw_data/test.csv',
    size=418,
    split_mode=['test'],
    split_ratio=[1.0],
    chunk_size=200000,
    features_names=[
        dict(name='Pclass', type='int', map=True),
        dict(name='Sex', map=True),
        dict(name='Age', type='int', map=False),
        dict(name='SibSp', type='int', map=False),
        dict(name='Parch', type='int', map=False),
        dict(name='Fare', type='float'),
        dict(name='Cabin', map=True),
        dict(name='Embarked', map=True),
    ]
)
other_train_files = []

# features settings
feature_mode = ['train']
target_name = 'Survived'
id_name = 'PassengerId'
feature_dict_file = feature_save_dir + "feature_dict_train.json"
draw_feature = True
style = 'darkgrid'

# train settings
work_dirs = "./work_dirs/"
dataset_name = "titanic"
balanced_data = False
normalization = 'none' # global, local, none
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
    dict(name='SVM', random_state=random_state, params=None),
    dict(name='ET', random_state=random_state, params=None),
    # dict(name='KNN', random_state=random_state, params=None),
]