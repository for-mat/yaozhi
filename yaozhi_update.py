# -*- coding:utf-8 -*-

import requests
import re
import time
import sys
import codecs
from bs4 import BeautifulSoup
import pymysql
import chardet
import json
import ssl



db = pymysql.connect(host='192.168.1.100', port=3306, user='root', passwd='123123', db='spider_yaozhi', charset='utf8')
cursor = db.cursor()


reload(sys)
sys.setdefaultencoding('utf-8')

def getinfo(i):
    url = 'https://db.yaozh.com/hmap/%s.html' % (str(i))
    headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
                'dnt': '1',
                'Connection': 'close',
                'upgrade-insecure-requests': '1',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'accept-language': 'zh-CN,zh;q=0.9'
            } # 设置user-agent
    requests.adapters.DEFAULT_RETRIES = 5
    r = requests.get(url, headers=headers, verify=False) # 获取页面，设置超时时间为30s
    r = r.text
    soup = BeautifulSoup(r, 'lxml')
    try:
        hospital_name = soup.select('span[class="toFindImg"]')[0].get_text().strip().encode('utf-8')
        return hospital_name
    except IndexError:
        return False

#a = getinfo(3)





def main():
    global num
    for num in range(43710,90000):
        name = getinfo(num)
#        try:
#            name = getinfo(num)
#        except:
#            global num
#            num = num-1
#            continue
        name = json.dumps(name, encoding="utf-8", ensure_ascii=False)
        print name
        #time.sleep(1)
        if name == 'false':
            continue
        else:
            cursor.execute('update hospital set hospital_number=%s where name=%s' %(num,name))
            db.commit()


main()






