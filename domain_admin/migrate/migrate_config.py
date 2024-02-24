# -*- coding: utf-8 -*-
"""
@File    : migrate_config.py
@Date    : 2023-10-16

数据库迁移配置
"""
from domain_admin.enums.version_enum import VersionEnum
from domain_admin.migrate.history import (
    migrate_140_alpha_to_140,
    migrate_1512_to_1513,
    migrate_143_to_144,
    migrate_1422_to_1423,
    migrate_1213_to_131,
    migrate_158_to_159,
    migrate_1413_to_1414,
    migrate_136_to_140_alpha,
    migrate_1523_to_1524,
    migrate_151_to_152,
    migrate_102_to_103,
    migrate_110_to_1212,
    migrate_145_to_146,
    migrate_1212_to_1213,
    migrate_1520_to_1521,
    migrate_154_to_155,
    migrate_106_to_110,
    migrate_1533_to_1534,
    migrate_162_to_163,
    migrate_168_to_169,
    migrate_1610_to_1611
)

# 参数说明
# local_versions 本地版本
# migrate_func 升级函数
# update_version 升级后的版本

MIGRATE_CONFIG = [
    # 1.0.0 1.0.1 1.0.2 => 1.0.3
    {
        'local_versions': [
            VersionEnum.Version_100,
            VersionEnum.Version_101,
            VersionEnum.Version_102,
        ],
        'migrate_func': migrate_102_to_103.execute_migrate,
        'update_version': VersionEnum.Version_103
    },

    # 2023-03-24
    # 1.0.3 1.0.4 1.0.5 1.0.6 => 1.1.0
    {
        'local_versions': [
            VersionEnum.Version_103,
            VersionEnum.Version_104,
            VersionEnum.Version_105,
            VersionEnum.Version_106,
        ],
        'migrate_func': migrate_106_to_110.execute_migrate,
        'update_version': VersionEnum.Version_110
    },

    # 2023-04-22
    # 1.1.0 => 1.2.12
    {
        'local_versions': [
            VersionEnum.Version_110,
            VersionEnum.Version_111,
            VersionEnum.Version_112,
            VersionEnum.Version_113,
            VersionEnum.Version_114,
            VersionEnum.Version_115,
            VersionEnum.Version_116,
            VersionEnum.Version_117,
            VersionEnum.Version_118,
            VersionEnum.Version_119,
            VersionEnum.Version_1110,
            VersionEnum.Version_120,
            VersionEnum.Version_121,
            VersionEnum.Version_122,
            VersionEnum.Version_123,
            VersionEnum.Version_124,
            VersionEnum.Version_128,
            VersionEnum.Version_129,
            VersionEnum.Version_1210,
            VersionEnum.Version_1211,
        ],
        'migrate_func': migrate_110_to_1212.execute_migrate,
        'update_version': VersionEnum.Version_1212
    },

    # 2023-04-26
    {
        'local_versions': [
            VersionEnum.Version_1212
        ],
        'migrate_func': migrate_1212_to_1213.execute_migrate,
        'update_version': VersionEnum.Version_1213
    },

    # 2023-06-03
    # 1.2.13 => 1.3.1
    {
        'local_versions': [
            VersionEnum.Version_1213,
            VersionEnum.Version_1214,
            VersionEnum.Version_1215,
            VersionEnum.Version_1216,
            VersionEnum.Version_1217,
            VersionEnum.Version_1218,
            VersionEnum.Version_1221,
            VersionEnum.Version_1222,
            VersionEnum.Version_1223
        ],
        'migrate_func': migrate_1213_to_131.execute_migrate,
        'update_version': VersionEnum.Version_131
    },

    # 2023-06-14
    # 1.3.1 => 1.4.0-alpha
    {
        'local_versions': [
            VersionEnum.Version_131,
            VersionEnum.Version_132,
            VersionEnum.Version_133,
            VersionEnum.Version_134,
            VersionEnum.Version_135,
            VersionEnum.Version_136,
        ],
        'migrate_func': migrate_136_to_140_alpha.execute_migrate,
        'update_version': VersionEnum.Version_140_alpha
    },

    # 2023-06-19
    # 1.4.0-alpha => 1.4.0
    {
        'local_versions': [
            VersionEnum.Version_140_alpha
        ],
        'migrate_func': migrate_140_alpha_to_140.execute_migrate,
        'update_version': VersionEnum.Version_140
    },

    # 2023-06-20
    # 1.4.0 => 1.4.4
    {
        'local_versions': [
            VersionEnum.Version_140,
            VersionEnum.Version_141,
            VersionEnum.Version_142,
            VersionEnum.Version_143,
            VersionEnum.Version_144,
        ],
        'migrate_func': migrate_143_to_144.execute_migrate,
        'update_version': VersionEnum.Version_144
    },

    # 2023-06-22
    # 1.4.4 => 1.4.6
    {
        'local_versions': [
            VersionEnum.Version_144,
            VersionEnum.Version_145,
        ],
        'migrate_func': migrate_145_to_146.execute_migrate,
        'update_version': VersionEnum.Version_146
    },

    # 2023-06-30
    # 1.4.6 => 1.4.14
    {
        'local_versions': [
            VersionEnum.Version_146,
            VersionEnum.Version_147,
            VersionEnum.Version_148,
            VersionEnum.Version_149,
            VersionEnum.Version_1410,
            VersionEnum.Version_1411,
            VersionEnum.Version_1412,
            VersionEnum.Version_1413,
            VersionEnum.Version_1414,
        ],
        'migrate_func': migrate_1413_to_1414.execute_migrate,
        'update_version': VersionEnum.Version_1414
    },

    # 2023-07-05
    # 1.4.22 => 1.4.23
    {
        'local_versions': [
            VersionEnum.Version_1414,
            VersionEnum.Version_1415,
            VersionEnum.Version_1416,
            VersionEnum.Version_1417,
            VersionEnum.Version_1418,
            VersionEnum.Version_1419,
            VersionEnum.Version_1420,
            VersionEnum.Version_1421,
            VersionEnum.Version_1422,
            VersionEnum.Version_1423,
        ],
        'migrate_func': migrate_1422_to_1423.execute_migrate,
        'update_version': VersionEnum.Version_1423
    },

    # 2023-07-19
    # 1.5.1 => 1.5.2
    {
        'local_versions': [
            VersionEnum.Version_1423,
            VersionEnum.Version_1424,
            VersionEnum.Version_1425,
            VersionEnum.Version_1426,
            VersionEnum.Version_1427,
            VersionEnum.Version_1428,
            VersionEnum.Version_1429,
            VersionEnum.Version_1430,
            VersionEnum.Version_1431,
            VersionEnum.Version_1432,
            VersionEnum.Version_1433,
            VersionEnum.Version_1434,
            VersionEnum.Version_1435,
            VersionEnum.Version_1436,
            VersionEnum.Version_150,
            VersionEnum.Version_151,
        ],
        'migrate_func': migrate_151_to_152.execute_migrate,
        'update_version': VersionEnum.Version_152
    },

    # 2023-07-22
    # 1.5.4 => 1.5.5
    {
        'local_versions': [
            VersionEnum.Version_152,
            VersionEnum.Version_153,
            VersionEnum.Version_154,
        ],
        'migrate_func': migrate_154_to_155.execute_migrate,
        'update_version': VersionEnum.Version_155
    },

    # 2023-07-22
    # 1.5.8 => 1.5.9
    {
        'local_versions': [
            VersionEnum.Version_155,
            VersionEnum.Version_156,
            VersionEnum.Version_157,
            VersionEnum.Version_158,
        ],
        'migrate_func': migrate_158_to_159.execute_migrate,
        'update_version': VersionEnum.Version_159
    },

    # 2023-08-03
    # 1.5.12 => 1.5.13
    {
        'local_versions': [
            VersionEnum.Version_159,
            VersionEnum.Version_1510,
            VersionEnum.Version_1511,
            VersionEnum.Version_1512,
        ],
        'migrate_func': migrate_1512_to_1513.execute_migrate,
        'update_version': VersionEnum.Version_1513
    },

    # 2023-08-30
    # 1.5.20 => 1.5.21
    {
        'local_versions': [
            VersionEnum.Version_1513,
            VersionEnum.Version_1514,
            VersionEnum.Version_1515,
            VersionEnum.Version_1516,
            VersionEnum.Version_1517,
            VersionEnum.Version_1518,
            VersionEnum.Version_1519,
            VersionEnum.Version_1520,
        ],
        'migrate_func': migrate_1520_to_1521.execute_migrate,
        'update_version': VersionEnum.Version_1521
    },

    # 2023-08-30
    # 1.5.23 => 1.5.24
    {
        'local_versions': [
            VersionEnum.Version_1521,
            VersionEnum.Version_1522,
            VersionEnum.Version_1523,
        ],
        'migrate_func': migrate_1523_to_1524.execute_migrate,
        'update_version': VersionEnum.Version_1524
    },

    # 2023-11-28
    # 1.5.33 => 1.5.34
    {
        'local_versions': [
            VersionEnum.Version_1524,
            VersionEnum.Version_1525,
            VersionEnum.Version_1526,
            VersionEnum.Version_1527,
            VersionEnum.Version_1528,
            VersionEnum.Version_1529,
            VersionEnum.Version_1530,
            VersionEnum.Version_1531,
            VersionEnum.Version_1532,
            VersionEnum.Version_1533,
        ],
        'migrate_func': migrate_1533_to_1534.execute_migrate,
        'update_version': VersionEnum.Version_1534
    },
    # 2024-01-28
    # 1.5.34 => 1.6.2
    {
        'local_versions': [
            VersionEnum.Version_1534,
            VersionEnum.Version_1535,
            VersionEnum.Version_1536,
            VersionEnum.Version_1537,
            VersionEnum.Version_1538,
            VersionEnum.Version_1539,
            VersionEnum.Version_160,
            VersionEnum.Version_161,
            VersionEnum.Version_162,
        ],
        'migrate_func': migrate_162_to_163.execute_migrate,
        'update_version': VersionEnum.Version_163
    },
    # 2024-02-20
    # 1.6.8 => 1.6.9
    {
        'local_versions': [
            VersionEnum.Version_163,
            VersionEnum.Version_164,
            VersionEnum.Version_165,
            VersionEnum.Version_166,
            VersionEnum.Version_167,
            VersionEnum.Version_168,
        ],
        'migrate_func': migrate_168_to_169.execute_migrate,
        'update_version': VersionEnum.Version_169
    },

    # 2024-02-24
    # 1.6.10 => 1.6.11
    {
        'local_versions': [
            VersionEnum.Version_169,
            VersionEnum.Version_1610,
        ],
        'migrate_func': migrate_1610_to_1611.execute_migrate,
        'update_version': VersionEnum.Version_1611
    },
]
