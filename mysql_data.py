# -*- coding: utf-8 -*-

'''
    药智全国医院数据库信息抓取导入mysql
'''

import os
from bs4 import BeautifulSoup
#import MySQLdb
import pymysql
import requests
import codecs

#CREATE TABLE `hospital` (   `id` int(11) NOT NULL AUTO_INCREMENT,   `name` varchar(30) DEFAULT NULL COMMENT '医院名称',   `alias` varchar(30) DEFAULT NULL COMMENT '医院别名',   `level` varchar(10) DEFAULT NULL COMMENT '医院等级',   `type` varchar(10) DEFAULT NULL COMMENT '医院类型',   `year` varchar(4) DEFAULT NULL COMMENT '建院年份',   `leader` varchar(10) DEFAULT NULL COMMENT '负责人',   `model` varchar(10) DEFAULT NULL COMMENT '经营方式',   `bed` varchar(10) DEFAULT NULL COMMENT '床位数',   `clinic` varchar(10) DEFAULT NULL COMMENT '门诊量(日)',   `province` varchar(10) DEFAULT NULL COMMENT '省',   `city` varchar(10) DEFAULT NULL COMMENT '市',   `county` varchar(10) DEFAULT NULL COMMENT '县',   `project` varchar(4000) DEFAULT NULL COMMENT '诊疗项目',   `office` varchar(4) DEFAULT NULL COMMENT '医院科室',   `staff` varchar(10) DEFAULT NULL COMMENT '员工数',   `device` varchar(2000) DEFAULT NULL COMMENT '医院设备',   `phone` varchar(30) DEFAULT NULL COMMENT '电话',   `address` varchar(40) DEFAULT NULL COMMENT '医院地址',   `postcode` varchar(10) DEFAULT NULL COMMENT '邮编',   `web` varchar(50) DEFAULT NULL COMMENT '医院网址',   `intro` text COMMENT '医院简介',   PRIMARY KEY (`id`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#db = MySQLdb.connect('localhost','root','123','yaozhi',charset='utf8')
#cursor=db.cursor()
db = pymysql.connect(host='192.168.1.100', port=3306, user='root', passwd='123123', db='yaozhi', charset='utf8')
cursor = db.cursor()


'''读取网页文件，并解析；
    返回两个值，其中all_elem是本网页中包含的所有列名的列表，后面用于判断网页中的某一个列名是否存在；
    soup是对网页的解析，后面check_colum需要通过soup.select定位存在的列的值
'''
def open_file(file):
    #path = '/root/htmls/%s' % (file)
    path='C:\\Users\\win7\\Desktop\\htmls\\%s' %(file)
    html = codecs.open(path, 'rb', encoding='utf-8').read()
    # f= codecs.open(path, encoding='UTF-8')
    # html= f.read()
    soup = BeautifulSoup(html, 'lxml')
    tags = soup.select('th[class="detail-table-th"]')
    all_elem = []
    for i in tags:
        a = i.string.strip()
        all_elem.append(a)
    return all_elem, soup

'''
    检查elem(例如 u'医院名称')是否存在，如果存在，往列表添加对应的值；
    如果不存在，添加空到列表
'''
def check_colum(elem, soup, all_elem):
    if elem in all_elem:
        num=all_elem.index(elem)
        value= soup.select('span[class="toFindImg"]')[num].get_text().strip().encode('utf-8')
        list_values.append(value.replace('"', '\\"'))
    else:
        list_values.append(None)



colum = [
    u'医院名称',
    u'医院别名',
    u'医院等级',
    u'医院类型',
    u'建院年份',
    u'负责人',
    u'经营方式',
    u'床位数',
    u'日诊量(日)',
    u'省',
    u'市',
    u'县',
    u'诊疗项目',
    u'医院科室',
    u'员工数',
    u'医院设备',
    u'电话',
    u'医院地址',
    u'邮编',
    u'医院网址',
    u'医院简介',
]

'''
    遍历所有文件
        遍历检查所有的列名并往列表添加数据
        列表转为元组，将元组插入mysql
'''
for f in os.listdir('C:\\Users\\win7\\Desktop\\htmls\\'):
    (all_elem, soup) = open_file(f)
    list_values=[]
    for i in colum:
        check_colum(i, soup, all_elem)
    tuple_values = tuple(list_values)
    try:
        cursor.execute('insert into hospital(name,alias,level,type,year,leader,model,bed,clinic,province,city,county,project,office,staff,device,phone,address,postcode,web,intro) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % tuple_values)
    except:
        print f
    db.commit()

