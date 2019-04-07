**试想有这么一个需求**
* 从一个job表里选出salary为100的职位名

用常见的命令式语言来做这个需求是这样的


    def get_salary(s, table):
        res = []
        for k in table:
            if k.salary == s:
                res.append(k)
        return res

* 而用sql来做是这样的

    select * from table where salary=s;

区别主要是因为python属于命令式语言，sql算声明式的，对于命令式语言来说要做一个事情，这个事情怎么做，这个过程要来自己写，而对   
于声明式语言来说重点是关注这个结果。xpath也是这样的。这也是为什么声明式语言更适合于并行计算（主要是因为这类语言抽象掉了过程细节）


再来看这么一条稍微复杂点的sql
假设有这么一个job表,里面主要有这么几个字段

    title, city, companyid，salary
    
查找某个城市，岗位数大于300的公司名&职位数，倒叙排列
写出来的sql语句大概如下：

    select xx, count(xx)
    from xx_table
    where constraint_expression
    group by column
    having constraint_expression
    order by column


**来看下这个语句是如何执行的**

    1. 首先要找到这个表，所以from后面的要先执行（如果有join之类的操作也在第一步执行）
    2. 找到相应的表后就要根据条件对数据进行过滤了
    3. 下一步是对数据按照sql中定义的字段进行group分组
    4. 对分组的数据进行一次过滤
    5. 将select需要的字段取出来
    6. 对结果进行排序


来手写一个执行sql语句的程序

从最简单的开始

    select * from table;
    
* 第一步，创建一个table

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

* 第二步，写一个select函数


    def select(name, table):
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
            res.append([getattr(t, n) for n in name])
        return res


添加最常用的 where子句

    select * from table where city='changzhi';
    
* 第三步，添加过滤


    def pfilter(row, condition):
        if condition:
            return eval(condition, {field: getattr(row, field) for field in row._fields})
        else:
            return True


按照公司名进行分组

    select companyid,count(title) from table where city='changzhi' group by companyid;

* 第四步，添加group

主要依靠俩函数，一个用来分组，一个用来返回结果

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
        pass

更进一步，添加一个构建表的对象


    class Table:
        pass

调用此对象，输出为人眼容易看的

    Table:  Job
    title   salary   city   companyid
    pydev    12    beijing    15
    c++dev    12    beijing    15



一些测试

    select companyid,title from job where city=='beijing'
    Table:  Job
    companyid   title
    15    pydev
    15    c++dev
    15    cdev
    
    select companyid,sum(salary) from job where city=='beijing' groupby companyid
    Table:  Job
    companyid   sum_salary
    15    36
    
    select companyid,count(title) from job where city=='beijing' groupby companyid
    Table:  Job
    companyid   count_title
    15    3

代码在这里
https://github.com/zhao94254/train/blob/master/sql.py
个人博客  
https://www.97up.cn  
