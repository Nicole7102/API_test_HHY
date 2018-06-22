#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging, os, sys
import time
from InterfaceTest import readData
from sendMail import sendMail

# 解决Pycharm的str默认ascii编码，改成utf8
reload(sys)
sys.setdefaultencoding('utf8')

# 此处使用python自带的logging模块，用来作为测试日志，记录测试中系统产生的信息。
logfilename = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))
log_file = os.path.join(os.getcwd(), 'log/'+logfilename+'.log')
log_format = '[%(asctime)s] [%(levelname)s] %(message)s'     # 配置log格式
logging.basicConfig(format=log_format, filename=log_file, filemode='w', level=logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter(log_format)
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


def main():
    errorTest = readData('TestCase/testCase.xlsx', 'User')
    if len(errorTest) > 0:
        print len(errorTest)
        html = '<html><body>接口自动化扫描，共有 ' + str(len(errorTest)) + ' 个异常接口，列表如下：' +\
               '</p><table><tr><th style="width:100px;text-align:left">    接口    ' \
               '</th><th style="width:50px;text-align:left">    状态    </th><th style="width:200px;text-align:left">' \
               '    接口地址    </th><th style="text-align:left">    接口返回值    </th></tr>'
        for test in errorTest:
            html = html + '<tr><td style="text-align:left">' + test[0] + '</td><td style="text-align:left">' + test[1] \
                   + '</td><td style="text-align:left">' + test[2] + '</td><td style="text-align:left">' + test[3] +\
                   '</td></tr>'
        sendMail(html)

if __name__ == '__main__':
    main()
