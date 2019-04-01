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

def select(name, table, condition=None):
    """
    :param name: 需要选的字段
    :param table: 表对象
    :return:
    """
    res = []
    if name == '*':
        name = table[0]._fields
    else:
        name = name.split(',')
    for t in table:
        if not pfilter(t, condition):
            continue
        res.append([getattr(t, n) for n in name])
    return res

def pfilter(row, condition):
    if condition:
        return eval(condition, {field: getattr(row, field) for field in row._fields})
    else:
        return True

if __name__ == '__main__':
    row = ('Row', 'name', 'age', 'location', 'money')
    data = [('jack', 12, 'beijing', 15),
            ('rose', 15, 'shanghai', 23),
            ('aha', 20, 'taiyuan', 345),
            ('liuxing', 18, 'changzhi', 432),
            ('luben', 18, 'shanghai', 233),
            ('douchuan', 18, 'changzhi', 322),
            ('heihai', 18, 'shanghai', 199), ]
    table = create_table(row, data)
    print(select('name', table, 'money>200'))