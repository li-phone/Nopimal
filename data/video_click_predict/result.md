# Video Click Predict Dataset

#### Train Introduction

train data size: 11376681

train valA valB ratio is 0.6: 0.2: 0.2

evaluation: f1 score

#### Validation Result

  
    balance: True
    normalization: local
    
	index   name	valA            valB
    3	LR	0.599409259	0.615131444
    5	RF	0.540743166	0.553215185
    2	GBT	0.540716934	0.549023837
    6	XGB	0.541298016	0.548099809
    7	ET	0.525851161	0.537367692
    4	GNB	0.529775966	0.535826127
    0	ABT	0.521969131	0.528789548
    1	DT	0.450620244	0.46117386



    balance: True
    normalization: global
    
	index   name	valA            valB
    5	RF	0.716025531	0.763444006
    3	LR	0.720924613	0.751993696
    2	GBT	0.708376511	0.746836355
    6	XGB	0.707646468	0.745112034
    0	ABT	0.697765704	0.735015317
    1	DT	0.675239354	0.724640846
    7	ET	0.681583842	0.713937238
    4	GNB	0.615041284	0.62076496



    balance: True
    normalization: global
    
	index   name	valA            valB
    5	RF	0.717117261	0.764369475
    3	LR	0.720804148	0.751794981
    2	GBT	0.708466198	0.746610202
    6	XGB	0.707568378	0.745003879
    0	ABT	0.70071987	0.737956505
    1	DT	0.67725012	0.726123673
    7	ET	0.67932611	0.712869278
    4	GNB	0.616158589	0.621908086

#### Summary
From the above result, we can see that these are not good.