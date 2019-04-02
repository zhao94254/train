# -*- coding: utf-8 -*-
# @Time    : 2019/4/1 20:57
# @Author  : py
# @Email   : zpy94254@gmail.com
# @File    : sql.py
# @Software: PyCharm

from collections import namedtuple, defaultdict

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

def select(name, table, condition=None, group_by=None):
    """
    :param name: 需要选的字段
    :param table: 表对象
    :return:
    """
    res = []
    tmp = []
    if name == '*':
        name = table[0]._fields
    else:
        name = name.split(',')
    for t in table:
        if not pfilter(t, condition):
            continue
        tmp.append(t)
    if group_by:
        _group = get_group(tmp, group_by)
    for t in tmp:
        res.append([getattr(t, n) for n in name])
    return res

def pfilter(row, condition):
    if condition:
        return eval(condition, {field: getattr(row, field) for field in row._fields})
    else:
        return True

def get_group(data, field):
    """
    将data按照field分组
    :param data:
    :param field:
    :return:
    """
    res = defaultdict(list)
    for d in data:
        res[getattr(d, field)].append(d)
    return res

if __name__ == '__main__':
    row = ('Job', 'title', 'salary', 'city', 'companyid')
    data = [('pydev', 12, 'beijing', 15),
            ('c++dev', 12, 'beijing', 15),
            ('cdev', 12, 'beijing', 15),
            ('pydev', 15, 'shanghai', 23),
            ('c++dev', 20, 'taiyuan', 345),
            ('pydev', 18, 'changzhi', 432),
            ('c++dev', 18, 'shanghai', 233),
            ('pydev', 18, 'changzhi', 322),
            ('javadev', 18, 'shanghai', 199), ]
    table = create_table(row, data)
    print(select('title,companyid', table, 'salary>15'))