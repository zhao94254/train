# -*- coding: utf-8 -*-
# @Time    : 2019/4/1 20:57
# @Author  : py
# @Email   : zpy94254@gmail.com
# @File    : sql.py
# @Software: PyCharm

from collections import namedtuple, defaultdict

class Table(object):

    def __init__(self, tname, rowname):
        self.tname = tname
        self.rowname = rowname

    def __call__(self, data):
        self.create_table(data)
        return self

    def create_table(self, data):
        table_row = namedtuple(self.tname, self.rowname)
        self.table = [table_row(*i) for i in data]
        return self.table

    def __str__(self):
        print('Table: ', self.tname)
        print('   '.join(self.rowname))
        for t in self.table:
            print('    '.join([str(getattr(t, i)) for i in self.rowname]))
        return ''

    __repr__ = __str__

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

def _select(field, tableobj, condition=None, group_by=None):
    """
    :param field: 需要选的字段
    :param table: 表对象
    :return:
    """
    res = []
    tmp = []
    table = tableobj.table
    if field == '*':
        field = table[0]._fields
    else:
        field = field.split(',')
    for t in table:
        if not pfilter(t, condition):
            continue
        tmp.append(t)
    if group_by:
        _group = get_group(tmp, group_by)
        res = get_group_data(_group, field, group_by)
        return res
    for t in tmp:
        res.append([getattr(t, n) for n in field])
    resobj = Table(tableobj.tname, (*field,))(res)
    return resobj

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

def get_group_data(groupdata,fds, groupby):
    res = []
    k1, k2 = 'NULL', 'NULL'
    for g in groupdata:
        if fds[0] == groupby:
            k1 = g
        k2 = s_group_data(fds[1], groupdata[g])
        res.append([k1, k2])
    return res

def s_group_data(fds, data):
    if fds.startswith('count('):
        return len(data)
    elif fds.startswith('sum('):
        return sum([getattr(i, fds[4:-1]) for i in data])
    return 'NULL'

def str_parse(sql):
    sql_obj = {}
    slst = sql.split()
    for k in range(len(slst)):
        if k%2 == 0:
            sql_obj[slst[k]] = slst[k+1]
    return sql_obj

def exec_sql(sql, table):
    sql_obj = str_parse(sql)
    return _select(sql_obj['select'], table, sql_obj.get('where', None), sql_obj.get('groupby', None))

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
    # table = create_table(row, data)
    # print(_select('companyid,count(title)', tojb.table, None, 'companyid'))

    tojb = Table('Job', ('title', 'salary', 'city', 'companyid'))(data) # 新的创建表的方式
    print(tojb)

    print(exec_sql("select companyid,count(title) from job where city=='beijing' groupby companyid", tojb))
    print(exec_sql("select companyid,count(title) from job groupby companyid", tojb))
    print(exec_sql("select companyid,sum(salary) from job where city=='beijing' groupby companyid", tojb))
    print(exec_sql("select companyid,title from job where city=='beijing'", tojb))
