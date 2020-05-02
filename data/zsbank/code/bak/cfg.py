# config

work_dirs = './work_dirs'
train_feature = './data/split_train_feature.csv'
val_feature = './data/split_val_feature.csv'
test_feature = './data/test_feature.csv'
test_csv = './data/test_tag.csv'

id_name = 'id'
target_name = 'flag'
balanced_data = False
normalization = 'none'
# global, local, none
random_state = 666

train_models = [
    dict(name='RF', random_state=random_state, params=dict()),
    dict(name='XGB', random_state=random_state, params=dict()),
    dict(name='LGB', random_state=random_state, params=dict()),
    dict(name='DT', random_state=random_state, params=dict()),
    dict(name='LR', random_state=random_state, params=dict()),
    dict(name='ET', random_state=random_state, params=dict()),
    dict(name='GBT', random_state=random_state, params=dict()),
    dict(name='GNB', random_state=random_state, params=dict()),
    # dict(name='ABT', random_state=random_state, params=dict()),
    # dict(name='SVM', random_state=random_state, params=dict()),
    # dict(name='KNN', random_state=random_state, params=None),
]
