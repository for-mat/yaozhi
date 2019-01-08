# -*- coding:utf-8 -*-

import requests
import re
import time
import sys
import codecs

reload(sys)
sys.setdefaultencoding('utf-8')


error_log=open('error.txt','ab')
def getHTMLText(url):
    '获取目标页面'
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'zh-CN,zh;q=0.9'
        } # 设置user-agent
        r = requests.get(url, headers=headers, timeout=30) # 获取页面，设置超时时间为30s
        r.raise_for_status() # 如果状态码不是200，引发HTTPError异常
        r.encoding = 'utf-8'  # 设置编码会页面的正确编码
        return r.text  # 如果需要二进制信息，应该使用r.content
    except:
        return False




for i in range(36515,82000):  # 爬取全部177页数据
    url = 'https://db.yaozh.com/hmap/%s.html' % (str(i))
    html = getHTMLText(url)
    if html == False:
        print i
        for vv in range(3):
            html = getHTMLText(url)
            if html != False:
                break
            time.sleep(3)
        if html == False:
            print i
            error_log.writelines(str(i)+'\n')


    htmls = codecs.open(str(i) + '.html', 'wb', 'utf-8')
    htmls.writelines(html)


'''
    s = u'医院名称'
    regex_str = s.encode('utf-8')
    match_obj = re.search(regex_str, html.encode('utf-8'))
    if not match_obj:
        for vv in range(2):
            html = getHTMLText(url)
            s = u'医院名称'
            regex_str = s.encode('utf-8')
            match_obj = re.search(regex_str, html.encode('utf-8'))
            if match_obj:
                break
            time.sleep(2)
        if not match_obj:
            print i
            print '3 times not find hospital name'
            error_log.writelines(str(i) + '\n')
    '''



