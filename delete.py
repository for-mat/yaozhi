# -*- coding: utf-8 -*-

import os


#a=0
error_log = open('err.txt', 'ab')
for i in range(1,82000):
    html = str(i) + '.html'

    if os.path.exists('C:\\Users\\win7\\Desktop\\htmls\\' + html):
        size = os.path.getsize('C:\\Users\\win7\\Desktop\\htmls\\' + html)

        if str(size) == '67354' or str(size) == '0':
            #a+=1
            error_log.writelines(str(i) + '\n')
            os.remove('C:\\Users\\win7\\Desktop\\htmls\\' + html)
#print a







