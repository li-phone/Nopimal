# global settings
data_root = "../../data/favorite_purchase_predict/"
feature_save_dir = data_root + "features/"
img_save_dir = data_root + "imgs/"

# split chunk settings
split_chunk_path = data_root + 'chunk/'
raw_train_file = dict(
    file_path=data_root + 'raw_data/train.csv',
    size=11000,
    split_mode=['train', 'valA', 'valB'],
    split_ratio=[0.6, 0.2, 0.2],
    chunk_size=200000,
    features_names=[
        {
            "name": "purchase",
            "type": "int"
        },
        {
            "name": "user_id",
            "map": True
        },
        {
            "name": "seller",
            "map": True
        },
        {
            "name": "Product_id",
            "map": True
        },
        {
            "name": "UserInfo_52",
            "type": "float"
        },
        {
            "name": "UserInfo_128",
            "type": "int"
        },
        {
            "name": "ProductInfo_194",
            "type": "int"
        },
        {
            "name": "UserInfo_70",
            "type": "int"
        },
        {
            "name": "UserInfo_266",
            "type": "int"
        },
        {
            "name": "UserInfo_244",
            "type": "int"
        },
        {
            "name": "UserInfo_250",
            "type": "float"
        },
        {
            "name": "UserInfo_246",
            "type": "int"
        },
        {
            "name": "UserInfo_217",
            "type": "float"
        },
        {
            "name": "ProductInfo_127",
            "type": "int"
        },
        {
            "name": "ProductInfo_9",
            "type": "int"
        },
        {
            "name": "ProductInfo_188",
            "type": "int"
        },
        {
            "name": "UserInfo_165",
            "type": "float"
        },
        {
            "name": "UserInfo_259",
            "type": "float"
        },
        {
            "name": "UserInfo_33",
            "type": "int"
        },
        {
            "name": "UserInfo_190",
            "type": "int"
        },
        {
            "name": "UserInfo_137",
            "type": "float"
        },
        {
            "name": "action_type",
            "type": "int"
        },
        {
            "name": "ProductInfo_99",
            "type": "int"
        },
        {
            "name": "ProductInfo_46",
            "type": "int"
        },
        {
            "name": "UserInfo_156",
            "type": "int"
        },
        {
            "name": "UserInfo_138",
            "type": "float"
        },
        {
            "name": "UserInfo_143",
            "type": "int"
        },
        {
            "name": "ProductInfo_106",
            "type": "int"
        },
        {
            "name": "UserInfo_253",
            "type": "int"
        },
        {
            "name": "UserInfo_94",
            "type": "float"
        },
        {
            "name": "UserInfo_4",
            "type": "float"
        },
        {
            "name": "ProductInfo_64",
            "type": "int"
        },
        {
            "name": "UserInfo_147",
            "type": "float"
        },
        {
            "name": "UserInfo_83",
            "type": "float"
        },
        {
            "name": "ProductInfo_123",
            "type": "int"
        },
        {
            "name": "ProductInfo_53",
            "type": "int"
        },
        {
            "name": "UserInfo_62",
            "type": "int"
        },
        {
            "name": "UserInfo_43",
            "type": "int"
        },
        {
            "name": "ProductInfo_129",
            "type": "int"
        },
        {
            "name": "UserInfo_13",
            "type": "int"
        },
        {
            "name": "ProductInfo_100",
            "type": "int"
        },
        {
            "name": "UserInfo_16",
            "type": "float"
        },
        {
            "name": "UserInfo_235",
            "type": "float"
        },
        {
            "name": "WebInfo_3",
            "type": "int"
        },
        {
            "name": "ProductInfo_11",
            "type": "int"
        },
        {
            "name": "UserInfo_9",
            "type": "float"
        },
        {
            "name": "UserInfo_79",
            "type": "int"
        },
        {
            "name": "UserInfo_119",
            "type": "int"
        },
        {
            "name": "UserInfo_238",
            "type": "float"
        },
        {
            "name": "UserInfo_216",
            "type": "int"
        },
        {
            "name": "UserInfo_80",
            "type": "float"
        },
        {
            "name": "UserInfo_151",
            "type": "int"
        },
        {
            "name": "ProductInfo_102",
            "type": "int"
        },
        {
            "name": "UserInfo_269",
            "type": "float"
        },
        {
            "name": "UserInfo_211",
            "type": "float"
        },
        {
            "name": "UserInfo_167",
            "type": "int"
        },
        {
            "name": "UserInfo_12",
            "type": "float"
        },
        {
            "name": "UserInfo_187",
            "type": "float"
        },
        {
            "name": "ProductInfo_152",
            "type": "int"
        },
        {
            "name": "UserInfo_6",
            "type": "int"
        },
        {
            "name": "UserInfo_15",
            "type": "float"
        },
        {
            "name": "ProductInfo_107",
            "type": "int"
        },
        {
            "name": "UserInfo_223",
            "type": "int"
        },
        {
            "name": "UserInfo_184",
            "type": "float"
        },
        {
            "name": "ProductInfo_128",
            "type": "int"
        },
        {
            "name": "ProductInfo_122",
            "type": "int"
        },
        {
            "name": "UserInfo_45",
            "type": "int"
        },
        {
            "name": "UserInfo_17",
            "type": "float"
        },
        {
            "name": "UserInfo_169",
            "type": "float"
        },
        {
            "name": "ProductInfo_201",
            "type": "int"
        },
        {
            "name": "day",
            "type": "int"
        },
        {
            "name": "ProductInfo_146",
            "type": "int"
        },
        {
            "name": "UserInfo_178",
            "type": "int"
        },
        {
            "name": "UserInfo_11",
            "type": "float"
        },
        {
            "name": "ProductInfo_40",
            "type": "int"
        },
        {
            "name": "UserInfo_27",
            "type": "float"
        },
        {
            "name": "UserInfo_226",
            "type": "int"
        },
        {
            "name": "ProductInfo_80",
            "type": "int"
        },
        {
            "name": "UserInfo_180",
            "type": "int"
        },
        {
            "name": "UserInfo_263",
            "type": "float"
        },
        {
            "name": "UserInfo_254",
            "type": "int"
        },
        {
            "name": "UserInfo_36",
            "type": "float"
        },
        {
            "name": "UserInfo_166",
            "type": "int"
        },
        {
            "name": "UserInfo_256",
            "type": "float"
        },
        {
            "name": "UserInfo_232",
            "type": "int"
        },
        {
            "name": "UserInfo_261",
            "type": "float"
        },
        {
            "name": "ProductInfo_39",
            "type": "int"
        },
        {
            "name": "UserInfo_219",
            "type": "int"
        },
        {
            "name": "UserInfo_168",
            "type": "int"
        },
        {
            "name": "UserInfo_195",
            "type": "float"
        },
        {
            "name": "ProductInfo_148",
            "type": "int"
        },
        {
            "name": "ProductInfo_81",
            "type": "int"
        },
        {
            "name": "ProductInfo_35",
            "type": "int"
        },
        {
            "name": "UserInfo_18",
            "type": "int"
        },
        {
            "name": "ProductInfo_19",
            "type": "int"
        },
        {
            "name": "ProductInfo_155",
            "type": "int"
        },
        {
            "name": "ProductInfo_163",
            "type": "int"
        },
        {
            "name": "ProductInfo_187",
            "type": "int"
        },
        {
            "name": "UserInfo_82",
            "type": "float"
        },
        {
            "name": "UserInfo_95",
            "type": "float"
        },
        {
            "name": "ProductInfo_212",
            "type": "int"
        },
        {
            "name": "UserInfo_2",
            "type": "float"
        },
        {
            "name": "ProductInfo_7",
            "type": "int"
        },
        {
            "name": "UserInfo_141",
            "type": "float"
        },
        {
            "name": "ProductInfo_133",
            "type": "int"
        },
        {
            "name": "ProductInfo_213",
            "type": "int"
        },
        {
            "name": "UserInfo_66",
            "type": "float"
        },
        {
            "name": "ProductInfo_74",
            "type": "int"
        },
        {
            "name": "ProductInfo_3",
            "type": "int"
        },
        {
            "name": "ProductInfo_24",
            "type": "int"
        },
        {
            "name": "UserInfo_24",
            "type": "int"
        },
        {
            "name": "ProductInfo_191",
            "type": "int"
        },
        {
            "name": "UserInfo_81",
            "type": "float"
        },
        {
            "name": "UserInfo_132",
            "type": "float"
        },
        {
            "name": "ProductInfo_73",
            "type": "int"
        },
        {
            "name": "ProductInfo_139",
            "type": "int"
        },
        {
            "name": "UserInfo_91",
            "type": "int"
        },
        {
            "name": "UserInfo_113",
            "type": "float"
        },
        {
            "name": "UserInfo_194",
            "type": "int"
        },
        {
            "name": "WebInfo_2",
            "type": "int"
        },
        {
            "name": "UserInfo_96",
            "type": "float"
        },
        {
            "name": "UserInfo_127",
            "type": "float"
        },
        {
            "name": "ProductInfo_6",
            "type": "int"
        },
        {
            "name": "ProductInfo_95",
            "type": "int"
        },
        {
            "name": "ProductInfo_182",
            "type": "int"
        },
        {
            "name": "UserInfo_58",
            "type": "int"
        },
        {
            "name": "UserInfo_69",
            "type": "int"
        },
        {
            "name": "ProductInfo_37",
            "type": "int"
        },
        {
            "name": "UserInfo_117",
            "type": "float"
        },
        {
            "name": "UserInfo_136",
            "type": "float"
        },
        {
            "name": "UserInfo_139",
            "type": "float"
        },
        {
            "name": "ProductInfo_198",
            "type": "int"
        },
        {
            "name": "UserInfo_159",
            "type": "float"
        },
        {
            "name": "ProductInfo_87",
            "type": "int"
        },
        {
            "name": "UserInfo_112",
            "type": "int"
        },
        {
            "name": "UserInfo_268",
            "type": "float"
        },
        {
            "name": "UserInfo_122",
            "type": "int"
        },
        {
            "name": "UserInfo_86",
            "type": "float"
        },
        {
            "name": "ProductInfo_77",
            "type": "int"
        },
        {
            "name": "UserInfo_22",
            "type": "int"
        },
        {
            "name": "UserInfo_98",
            "type": "int"
        },
        {
            "name": "ProductInfo_134",
            "type": "int"
        },
        {
            "name": "UserInfo_176",
            "type": "int"
        },
        {
            "name": "ProductInfo_156",
            "type": "int"
        },
        {
            "name": "UserInfo_198",
            "type": "int"
        },
        {
            "name": "ProductInfo_101",
            "type": "int"
        },
        {
            "name": "ProductInfo_92",
            "type": "int"
        },
        {
            "name": "UserInfo_183",
            "type": "int"
        },
        {
            "name": "UserInfo_14",
            "type": "int"
        },
        {
            "name": "ProductInfo_160",
            "type": "int"
        },
        {
            "name": "UserInfo_230",
            "type": "int"
        },
        {
            "name": "ProductInfo_173",
            "type": "int"
        },
        {
            "name": "UserInfo_19",
            "type": "float"
        },
        {
            "name": "UserInfo_174",
            "type": "int"
        },
        {
            "name": "UserInfo_30",
            "type": "int"
        },
        {
            "name": "UserInfo_28",
            "type": "float"
        },
        {
            "name": "UserInfo_37",
            "type": "float"
        },
        {
            "name": "UserInfo_34",
            "type": "int"
        },
        {
            "name": "UserInfo_51",
            "type": "int"
        },
        {
            "name": "UserInfo_270",
            "type": "float"
        },
        {
            "name": "UserInfo_38",
            "type": "int"
        },
        {
            "name": "UserInfo_222",
            "type": "int"
        },
        {
            "name": "UserInfo_267",
            "type": "float"
        },
        {
            "name": "UserInfo_205",
            "type": "int"
        },
        {
            "name": "UserInfo_171",
            "type": "int"
        },
        {
            "name": "ProductInfo_110",
            "type": "int"
        },
        {
            "name": "UserInfo_231",
            "type": "float"
        },
        {
            "name": "UserInfo_116",
            "type": "int"
        },
        {
            "name": "UserInfo_188",
            "type": "float"
        },
        {
            "name": "UserInfo_145",
            "type": "int"
        },
        {
            "name": "ProductInfo_45",
            "type": "int"
        },
        {
            "name": "ProductInfo_138",
            "type": "int"
        },
        {
            "name": "UserInfo_206",
            "type": "float"
        },
        {
            "name": "UserInfo_154",
            "type": "int"
        },
        {
            "name": "UserInfo_61",
            "type": "int"
        },
        {
            "name": "UserInfo_243",
            "type": "int"
        },
        {
            "name": "UserInfo_21",
            "type": "float"
        },
        {
            "name": "UserInfo_78",
            "type": "int"
        },
        {
            "name": "ProductInfo_84",
            "type": "int"
        },
        {
            "name": "UserInfo_197",
            "type": "float"
        },
        {
            "name": "UserInfo_10",
            "type": "int"
        },
        {
            "name": "UserInfo_123",
            "type": "int"
        },
        {
            "name": "UserInfo_63",
            "type": "float"
        },
        {
            "name": "UserInfo_181",
            "type": "int"
        },
        {
            "name": "UserInfo_31",
            "type": "int"
        },
        {
            "name": "ProductInfo_114",
            "type": "int"
        },
        {
            "name": "UserInfo_107",
            "type": "int"
        },
        {
            "name": "UserInfo_50",
            "type": "int"
        },
        {
            "name": "UserInfo_97",
            "type": "float"
        },
        {
            "name": "ProductInfo_58",
            "type": "int"
        },
        {
            "name": "ProductInfo_62",
            "type": "int"
        },
        {
            "name": "UserInfo_234",
            "type": "float"
        },
        {
            "name": "UserInfo_41",
            "type": "int"
        },
        {
            "name": "UserInfo_100",
            "type": "float"
        },
        {
            "name": "UserInfo_74",
            "type": "int"
        },
        {
            "name": "ProductInfo_203",
            "type": "int"
        },
        {
            "name": "UserInfo_42",
            "type": "int"
        },
        {
            "name": "ProductInfo_125",
            "type": "int"
        },
        {
            "name": "UserInfo_109",
            "type": "int"
        },
        {
            "name": "UserInfo_46",
            "type": "int"
        },
        {
            "name": "UserInfo_68",
            "type": "int"
        },
        {
            "name": "UserInfo_57",
            "type": "float"
        },
        {
            "name": "UserInfo_140",
            "type": "int"
        },
        {
            "name": "UserInfo_152",
            "type": "float"
        },
        {
            "name": "UserInfo_160",
            "type": "float"
        },
        {
            "name": "ProductInfo_190",
            "type": "int"
        },
        {
            "name": "UserInfo_201",
            "type": "float"
        },
        {
            "name": "UserInfo_134",
            "type": "float"
        },
        {
            "name": "UserInfo_189",
            "type": "float"
        },
        {
            "name": "UserInfo_114",
            "type": "int"
        },
        {
            "name": "UserInfo_48",
            "type": "int"
        },
        {
            "name": "UserInfo_153",
            "type": "float"
        },
        {
            "name": "ProductInfo_168",
            "type": "int"
        },
        {
            "name": "UserInfo_262",
            "type": "int"
        },
        {
            "name": "UserInfo_67",
            "type": "float"
        },
        {
            "name": "UserInfo_251",
            "type": "float"
        },
        {
            "name": "UserInfo_124",
            "type": "int"
        },
        {
            "name": "UserInfo_179",
            "type": "float"
        },
        {
            "name": "ProductInfo_116",
            "type": "int"
        },
        {
            "name": "UserInfo_73",
            "type": "float"
        },
        {
            "name": "UserInfo_1",
            "type": "float"
        },
        {
            "name": "UserInfo_245",
            "type": "float"
        },
        {
            "name": "UserInfo_105",
            "type": "float"
        },
        {
            "name": "UserInfo_71",
            "type": "float"
        },
        {
            "name": "ProductInfo_42",
            "type": "int"
        },
        {
            "name": "UserInfo_87",
            "type": "int"
        },
        {
            "name": "ProductInfo_94",
            "type": "int"
        },
        {
            "name": "UserInfo_264",
            "type": "int"
        },
        {
            "name": "UserInfo_191",
            "type": "int"
        },
        {
            "name": "UserInfo_125",
            "type": "float"
        },
        {
            "name": "UserInfo_7",
            "type": "float"
        },
        {
            "name": "ProductInfo_96",
            "type": "int"
        },
        {
            "name": "ProductInfo_137",
            "type": "int"
        },
        {
            "name": "UserInfo_209",
            "type": "int"
        },
        {
            "name": "UserInfo_56",
            "type": "float"
        },
        {
            "name": "ProductInfo_104",
            "type": "int"
        },
        {
            "name": "ProductInfo_157",
            "type": "int"
        },
        {
            "name": "ProductInfo_169",
            "type": "int"
        },
        {
            "name": "UserInfo_35",
            "type": "int"
        },
        {
            "name": "UserInfo_172",
            "type": "float"
        },
        {
            "name": "UserInfo_8",
            "type": "float"
        },
        {
            "name": "UserInfo_88",
            "type": "float"
        },
        {
            "name": "ProductInfo_89",
            "type": "float"
        },
        {
            "name": "UserInfo_130",
            "type": "float"
        },
        {
            "name": "UserInfo_3",
            "type": "float"
        },
        {
            "name": "UserInfo_239",
            "type": "int"
        },
        {
            "name": "ProductInfo_124",
            "type": "int"
        },
        {
            "name": "UserInfo_89",
            "type": "int"
        },
        {
            "name": "ProductInfo_136",
            "type": "int"
        },
        {
            "name": "UserInfo_25",
            "type": "float"
        },
        {
            "name": "ProductInfo_18",
            "type": "int"
        },
        {
            "name": "ProductInfo_184",
            "type": "int"
        },
        {
            "name": "UserInfo_252",
            "type": "int"
        },
        {
            "name": "UserInfo_177",
            "type": "int"
        },
        {
            "name": "UserInfo_186",
            "type": "float"
        },
        {
            "name": "UserInfo_5",
            "type": "float"
        },
        {
            "name": "UserInfo_77",
            "type": "int"
        },
        {
            "name": "UserInfo_265",
            "type": "int"
        },
        {
            "name": "UserInfo_150",
            "type": "int"
        },
        {
            "name": "UserInfo_213",
            "type": "float"
        },
        {
            "name": "UserInfo_240",
            "type": "float"
        },
        {
            "name": "UserInfo_258",
            "type": "float"
        },
        {
            "name": "UserInfo_212",
            "type": "int"
        },
        {
            "name": "UserInfo_236",
            "type": "int"
        },
        {
            "name": "ProductInfo_166",
            "type": "int"
        },
        {
            "name": "UserInfo_131",
            "type": "int"
        },
        {
            "name": "UserInfo_144",
            "type": "float"
        },
        {
            "name": "UserInfo_148",
            "type": "float"
        },
        {
            "name": "UserInfo_59",
            "type": "float"
        },
        {
            "name": "ProductInfo_29",
            "type": "int"
        },
        {
            "name": "UserInfo_237",
            "type": "float"
        },
        {
            "name": "UserInfo_257",
            "type": "int"
        },
        {
            "name": "UserInfo_55",
            "type": "int"
        },
        {
            "name": "UserInfo_60",
            "type": "float"
        },
        {
            "name": "UserInfo_164",
            "type": "int"
        },
        {
            "name": "UserInfo_118",
            "type": "float"
        },
        {
            "name": "UserInfo_106",
            "type": "float"
        },
        {
            "name": "ProductInfo_54",
            "type": "int"
        },
        {
            "name": "UserInfo_92",
            "type": "float"
        },
        {
            "name": "UserInfo_225",
            "type": "int"
        },
        {
            "name": "UserInfo_242",
            "type": "float"
        },
        {
            "name": "UserInfo_108",
            "type": "int"
        },
        {
            "name": "UserInfo_40",
            "type": "int"
        },
        {
            "name": "ProductInfo_215",
            "type": "int"
        },
        {
            "name": "ProductInfo_2",
            "type": "int"
        },
        {
            "name": "UserInfo_20",
            "type": "float"
        },
        {
            "name": "ProductInfo_51",
            "type": "int"
        },
        {
            "name": "UserInfo_227",
            "type": "float"
        },
        {
            "name": "UserInfo_23",
            "type": "int"
        },
        {
            "name": "UserInfo_196",
            "type": "float"
        },
        {
            "name": "UserInfo_155",
            "type": "float"
        },
        {
            "name": "ProductInfo_63",
            "type": "int"
        },
        {
            "name": "UserInfo_199",
            "type": "float"
        },
        {
            "name": "ProductInfo_141",
            "type": "int"
        },
        {
            "name": "ProductInfo_90",
            "type": "int"
        },
        {
            "name": "UserInfo_210",
            "type": "float"
        },
        {
            "name": "UserInfo_26",
            "type": "int"
        },
        {
            "name": "UserInfo_228",
            "type": "int"
        },
        {
            "name": "UserInfo_120",
            "type": "int"
        },
        {
            "name": "ProductInfo_178",
            "type": "int"
        },
        {
            "name": "UserInfo_85",
            "type": "float"
        },
        {
            "name": "UserInfo_221",
            "type": "int"
        },
        {
            "name": "ProductInfo_50",
            "type": "int"
        },
        {
            "name": "UserInfo_104",
            "type": "float"
        },
        {
            "name": "UserInfo_248",
            "type": "float"
        },
        {
            "name": "UserInfo_247",
            "type": "int"
        },
        {
            "name": "UserInfo_218",
            "type": "float"
        },
        {
            "name": "UserInfo_39",
            "type": "int"
        },
        {
            "name": "UserInfo_110",
            "type": "int"
        },
        {
            "name": "UserInfo_214",
            "type": "int"
        },
        {
            "name": "UserInfo_204",
            "type": "int"
        },
        {
            "name": "UserInfo_157",
            "type": "float"
        },
        {
            "name": "UserInfo_93",
            "type": "int"
        },
        {
            "name": "ProductInfo_210",
            "type": "int"
        },
        {
            "name": "UserInfo_241",
            "type": "int"
        },
        {
            "name": "ProductInfo_4",
            "type": "int"
        },
        {
            "name": "UserInfo_75",
            "type": "float"
        },
        {
            "name": "ProductInfo_10",
            "type": "int"
        },
        {
            "name": "ProductInfo_44",
            "type": "int"
        },
        {
            "name": "WebInfo_1",
            "type": "int"
        },
        {
            "name": "UserInfo_32",
            "type": "int"
        },
        {
            "name": "UserInfo_111",
            "type": "int"
        },
        {
            "name": "UserInfo_64",
            "type": "int"
        },
        {
            "name": "UserInfo_133",
            "type": "float"
        },
        {
            "name": "UserInfo_49",
            "type": "float"
        },
        {
            "name": "UserInfo_170",
            "type": "int"
        },
        {
            "name": "UserInfo_162",
            "type": "int"
        },
        {
            "name": "UserInfo_229",
            "type": "float"
        },
        {
            "name": "ProductInfo_8",
            "type": "int"
        },
        {
            "name": "UserInfo_193",
            "type": "float"
        },
        {
            "name": "UserInfo_149",
            "type": "int"
        },
        {
            "name": "ProductInfo_199",
            "type": "int"
        },
        {
            "name": "UserInfo_44",
            "type": "float"
        },
        {
            "name": "ProductInfo_179",
            "type": "int"
        },
        {
            "name": "UserInfo_101",
            "type": "float"
        },
        {
            "name": "ProductInfo_108",
            "type": "int"
        },
        {
            "name": "UserInfo_224",
            "type": "int"
        },
        {
            "name": "UserInfo_255",
            "type": "int"
        },
        {
            "name": "UserInfo_163",
            "type": "int"
        },
        {
            "name": "UserInfo_146",
            "type": "float"
        },
        {
            "name": "UserInfo_158",
            "type": "int"
        },
        {
            "name": "UserInfo_121",
            "type": "float"
        },
        {
            "name": "UserInfo_29",
            "type": "float"
        },
        {
            "name": "UserInfo_175",
            "type": "int"
        },
        {
            "name": "UserInfo_182",
            "type": "int"
        }
    ]
)
raw_test_file = dict(
    file_path=data_root + 'raw_data/test.csv',
    size=3366,
    split_mode=[],
    split_ratio=[],
    chunk_size=200000,
    features_names=[]
)
other_train_files = []

# features settings
feature_mode = ['train']
target_name = 'purchase'
id_name = 'PassengerId'
feature_dict_file = feature_save_dir + "feature_dict_train.json"
draw_feature = True
style = 'darkgrid'

# train settings
work_dirs = "./work_dirs/"
dataset_name = "favorite_purchase_predict"
balanced_data = False
normalization = 'none' # global, local, none
random_state = 666
train_mode = ['train']
val_mode = ['valA', 'valB']
train_models = [
    dict(name='ABT', random_state=random_state, params=None),
    dict(name='DT', random_state=random_state, params=None),
    dict(name='GBT', random_state=random_state, params=None),
    # dict(name='KNN', random_state=random_state, params=None),
    dict(name='LR', random_state=random_state, params=None),
    dict(name='GNB', random_state=random_state, params=None),
    dict(name='RF', random_state=random_state, params=None),
    # dict(name='SVM', random_state=random_state, params=None),
    dict(name='XGB', random_state=random_state, params=None),
    dict(name='ET', random_state=random_state, params=None),
]
