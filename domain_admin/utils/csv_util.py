# -*- coding: utf-8 -*-
"""
@File    : csv_util.py
@Date    : 2023-10-14
"""
import io
import csv


def read_csv(filename):
    """
    读取csv文件 适合完整导入
    :param filename: str
    :return: iterator
    """
    with io.open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def write_csv(filename, rows):
    """
    读取csv文件 适合完整导入
    :param rows: list
    :param filename: str
    :return:
    """
    if len(rows) == 0:
        return

    with open(filename, "w") as f:
        writer = csv.DictWriter(f, rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


if __name__ == '__main__':
    # write_csv('./demo.csv', [
    #     {'name': 'Tom', 'age': 23},
    #     {'name': 'Jack', 'age': 24},
    # ])

    for row in read_csv('./demo.csv'):
        print(row)
