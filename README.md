# Nopimal
"Nopimal", "Nopi" or "诺派", No Pain in Machine Learning. This project aims to simplify the machine learning producer and obtains the not bad result. Welcome DaLao to join us and give us some advices.


#### Structure

1.  Split dataset to the chunks
2.  According to chunks, generate the feature dictionary
3.  Map feature dictionary to features
4.  Using features to train the data
5.  Infer the unknown data

#### Get Started

    python main.py

#### Test Result

**Titanic Dataset**

    train data size: 891
    train valA valB ratio: 0.6: 0.2: 0.2
    evaluation: f1 score
    
    id  name	valA	valB
    1	RF	0.718304906	0.797179889
    7	GNB	0.747159091	0.791724285
    2	XGB	0.705460563	0.726081898
    9	ET	0.714305228	0.721122347
    6	LR	0.670417319	0.720878136
    4	LGB	0.661299766	0.712720039
    5	DT	0.613423007	0.707586619
    3	GBT	0.660409035	0.685178635
    0	ABT	0.637163394	0.655549232
    8	SVM	0.623147495	0.623147495


#### License
This project is licensed under the MIT license.
