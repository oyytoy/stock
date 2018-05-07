#-*-coding:utf-8-*-

import os
import datetime
import sys
import pymysql
import subprocess
import db
import sendmail

to_mail_list = "ouyangyt@mmbrk.com;lifu@mmbrk.com"

def select_1():

    alias = ["经纪人","姓名","股票代码","委托时间","委托方向","委托币种","委托价格","已成交数量"]
    sql = """
           SELECT IFNULL(c.name,d.channel_name) 经纪人,b.name 姓名,stock_code 股票代码
           ,entrust_datetime 委托时间,CASE WHEN entrust_bs=0 THEN '买' WHEN entrust_bs=1 THEN '卖' WHEN entrust_bs=2 THEN 'short' END 委托方向
           ,CASE WHEN currency=0 THEN '港币' WHEN currency=1 THEN '美金' WHEN currency=2 THEN '人民币' END 委托币种
           ,CASE WHEN entrust_order_type=1 THEN latest_filled_price WHEN entrust_order_type!=1 THEN entrust_price END 委托价格
           ,filled_amount 已成交数量  FROM trade_entrust_order a LEFT JOIN customer_info b ON a.customer_no=b.customer_no 
           LEFT JOIN broker_info c ON  b.broker_id = c.id
           LEFT JOIN channel_info d ON b.channel_id=d.channel_id WHERE    a.local_order_type = 0 AND a.is_preview_order = 1 AND a.filled_amount!=0  
           AND c.name LIKE '浙江财富%'
    """

    db.query(sql,alias,'浙江财富.csv')

    sendmail.send_mail(to_mail_list,u'浙江财富.csv')

def select_2():

    alias = ["经纪人/渠道","姓名","股票代码","委托时间","委托方向","委托币种","委托价格","已成交数量"]
    sql = """
          SELECT IFNULL(c.name,d.channel_name) 经纪人,b.name 姓名,stock_code 股票代码
           ,entrust_datetime 委托时间,CASE WHEN entrust_bs=0 THEN '买' WHEN entrust_bs=1 THEN '卖' WHEN entrust_bs=2 THEN 'short' END 委托方向
           ,CASE WHEN currency=0 THEN '港币' WHEN currency=1 THEN '美金' WHEN currency=2 THEN '人民币' END 委托币种
           ,CASE WHEN entrust_order_type=1 THEN latest_filled_price WHEN entrust_order_type!=1 THEN entrust_price END 委托价格
           ,filled_amount 已成交数量  FROM trade_entrust_order a LEFT JOIN customer_info b ON a.customer_no=b.customer_no 
           LEFT JOIN broker_info c ON  b.broker_id = c.id
           LEFT JOIN channel_info d ON b.channel_id=d.channel_id WHERE    a.local_order_type = 0 AND a.is_preview_order = 1 AND a.filled_amount!=0
    """

    db.query(sql,alias,'全量.csv')

    sendmail.send_mail(to_mail_list,u'全量.csv')

def select():
    select_1()

    select_2()

    


if __name__ == '__main__':
    select()
