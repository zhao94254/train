# -*- coding: utf-8 -*-
# @Time    : 2019/4/1 20:57
# @Author  : py
# @Email   : zpy94254@gmail.com
# @File    : sql.py
# @Software: PyCharm

from collections import namedtuple

def create_table(row, data):
    """
    row[0] 表名  row[1:] 列名 data 要插入的数据
    :param row: ['Job', 'salary', 'name', 'city']
    :param data: [[100, dev, cz]]
    :return:
    """
    table_row = namedtuple(row[0], row[1:])
    table = [table_row(*i) for i in data]
    return table