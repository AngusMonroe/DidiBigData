#!/usr/bin/python3

import pymysql
from tqdm import tqdm

# 打开数据库连接
db = pymysql.connect(host='10.251.254.54', port=3306, user='didi', passwd='123456@BigData', db='data', charset='utf8')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()


def db2csv(out_path='../data/didi.csv'):
    print('Transfer start.')

    # 使用 execute()  方法执行 SQL 查询
    cursor.execute("select table_name from information_schema.tables where table_schema='data'")
    # 使用 fetchone() 方法获取单条数据.
    # data = cursor.fetchone()
    table_names = cursor.fetchall()

    file = open(out_path, 'w', encoding='utf8')

    for table_name in table_names:
        print(table_name[0])
        cursor.execute("SELECT * FROM data." + table_name[0])
        res = cursor.fetchall()
        for line in tqdm(res):
            file.write(table_name[0])
            for i in range(len(line)):
                file.write(',' + str(line[i]))
            file.write('\n')
        break

    file.close()
    print('Done!')

db2csv()
# 关闭数据库连接
db.close()