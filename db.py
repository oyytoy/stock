#-*-coding:utf-8-*-
import os
import datetime
import sys
import pymysql
import csv

# 数据库连接
db_host = '172.17.202.200'
db_user = 'root'
db_passwd = 'snr0clOxTpFhPp3P'
db_name = 'kernel'
db_port = 6004

def open_conn():
    conn = pymysql.connect(db_host, # your host, usually localhost
                     db_user, # your username
                     db_passwd, # your password
                     db_name, # name of the data base
                           port=db_port,
                           charset='utf8'
                     )
    return conn

def closeConnnection(conn):
    """
    关闭当前连接
    """
    conn.close()     

def query(sql,alias,fileName):
    conn = open_conn()
    cur=conn.cursor(pymysql.cursors.DictCursor)
    cur.execute(sql)
    results=cur.fetchall()
    #print title
    with open(fileName, 'w', newline='') as f:
        writer = csv.DictWriter(f,alias)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    # for r in results:
    #     for key in alias:
    #         print(str(r[key]))

    conn.commit()
    cur.close()
    closeConnnection(conn)
    return

def select_test():
    sql = "select id 编号,account 账号,password 密码,name 名称 from broker_info limit 10"
    query(sql,["编号","账号","密码","名称"],"test.cvs")

def select_1():

    alias = ["经纪人","姓名","股票代码","委托时间","委托方向","委托币种","委托价格","已成交数量"]
    sql = """
           SELECT c.name 经纪人,b.name 姓名,stock_code 股票代码
               ,entrust_datetime 委托时间,CASE WHEN entrust_bs=0 THEN '买' WHEN entrust_bs=1 THEN '卖' WHEN entrust_bs=2 THEN 'short' END 委托方向
               ,CASE WHEN currency=0 THEN '港币' WHEN currency=1 THEN '美金' WHEN currency=2 THEN '人民币' END 委托币种
               ,CASE WHEN entrust_order_type=1 THEN latest_filled_price WHEN entrust_order_type!=1 THEN entrust_price END 委托价格
              ,filled_amount 已成交数量  FROM trade_entrust_order a,customer_info b,broker_info c WHERE a.customer_no=b.customer_no AND  a.local_order_type = 0 AND a.is_preview_order = 1 AND a.filled_amount!=0 
             AND b.broker_id = c.id AND c.name LIKE '浙江财富%'
    """
    
    query(sql,alias,'浙江财富.csv')

if __name__ == '__main__':
    # select_test()
    select_1()
