# config
root_dir = '../work_dirs/zsbank/'
Trainer = dict(
    model_dir=root_dir + 'models/',
    train=dict(file=root_dir + 'data/split_train_feature.csv', target_key='flag'),
    val=dict(file=root_dir + 'data/split_val_feature.csv', target_key='flag'),
    log_file=root_dir + 'models/train_log.txt',
    normalize_type='StandardScaler',
    balance_data=False,
    stack_meta='LGB',
    models=[
        dict(name='RF', type='RF', random_state=666, params=dict(),
             param_grid={
                 'n_estimators': [800],
                 'max_depth': [9],
                 # 'criterion': ['entropy'],
                 # 'min_samples_split': [7]
             }),
        dict(name='XGB', type='XGB', random_state=666, params=dict(),
             param_grid={
                 'n_estimators': [40],
                 'max_depth': [6]
             }),
        dict(name='LGB', type='LGB', random_state=666, params=dict(),
             param_grid={
                 'n_estimators': [60],
             }),
        # dict(name='DT', type='DT', random_state=666, params=dict(),
        #      param_grid=dict(
        #          max_depth=[8],
        #          min_samples_split=[450]
        #      )),
        # dict(name='LR', type='LR', random_state=666, params=dict(),
        #      param_grid=dict(
        #          penalty=['l2'],
        #          C=[0.01]
        #      )),
        # dict(name='ET', type='ET', random_state=666, params=dict(),
        #      param_grid={
        #          'max_depth': list(range(6, 10))
        #      }),
        # dict(name='GBT', type='GBT', random_state=666, params=dict(),
        #      param_grid={
        #          # 'max_depth': list(range(3, 10)),
        #          # 'n_estimators': list(range(100, 800, 100)),
        #      }),
        # dict(name='GNB', type='GNB', random_state=666, params=dict(),
        #      param_grid={}),
        # dict(name='SVM_linear', type='SVM', random_state=666, params=dict(kernel='linear', probability=True),
        #      param_grid=dict(C=[0.01, 0.05, 0.1, 0.5, 1.])),
        # dict(name='SVM_poly', type='SVM', random_state=666, params=dict(kernel='poly', probability=True),
        #      param_grid=dict(C=[0.01, 0.05, 0.1, 0.5, 1.])),
        # dict(name='SVM_rbf', type='SVM', random_state=666, params=dict(kernel='rbf', probability=True),
        #      param_grid=dict(C=[0.01, 0.05, 0.1, 0.5, 1.])),
        # dict(name='SVM_sigmoid', type='SVM', random_state=666, params=dict(kernel='sigmoid', probability=True),
        #      param_grid=dict(C=[0.01, 0.05, 0.1, 0.5, 1.])),
        # dict(name='ABT', random_state=random_state, params=dict()),
        # dict(name='KNN', random_state=random_state, params=None),
    ]
)

Inference = dict(
    model_dir=root_dir + 'models/',
    submit_dir=root_dir + 'submit/',
    test=dict(file=root_dir + 'data/test_feature.csv', target_key='flag', uid_key='id'),
    normalize_type='StandardScaler',
    models=[
        dict(name='LGB_finetune', type='LGB'),
        dict(name='RF_finetune', type='RF'),
        dict(name='XGB_finetune', type='XGB'),
        dict(name='stacking_models', type='stack_model'),

        dict(name='LGB', type='LGB'),
        dict(name='RF', type='RF'),
        dict(name='XGB', type='XGB'),

        # dict(name='DT', type='DT'),
        # dict(name='LR', type='LR'),
        # dict(name='ET', type='ET'),
        # dict(name='GBT', type='GBT'),
        # dict(name='GNB', type='GNB'),
        # dict(name='SVM_linear', type='SVM'),
        # dict(name='SVM_poly', type='SVM'),
        # dict(name='SVM_rbf', type='SVM'),
        # dict(name='SVM_sigmoid', type='SVM'),
        # dict(name='ABT', type='ABT'),
        # dict(name='KNN', type='KNN'),
    ]
)
