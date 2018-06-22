#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests, json, re
import os, logging, sys, xlrd
import random


def createPhone():
    prelist = ["130","131","132","133","134","135","136","137","138","139","145","147","150","151","152","153","155","156","157","158","159","186","187","188"]
    phonenum = random.choice(prelist)+"".join(random.choice("0123456789") for i in range(8))
    return phonenum


def getVerificationCode(resp):
    vcode = str(json.loads(resp.text)[u'vcode'])
    return vcode


def interfaceTest(num, api_purpose, api_host, request_url, request_method, request_data, check_point):
    if request_url != "/hhyAppServer/getVerificationCode":
        if request_method == "Post":
            r = requests.post(url=api_host+request_url, data=json.loads(request_data))
            print r.text
        elif request_method == "Get":
            r = requests.get(url=api_host+request_url, data=json.loads(request_data))
        else:
            logging.error(num+' '+api_purpose+'HTTP请求方法错误，请确认Request Method字段是否正确！')
            return 400, None
    else:
        payload = {
            "phonenumber": createPhone()
        }
        r = requests.post(url=api_host+request_url, data=payload)
        vcode = getVerificationCode(r)
        status = r.status_code
        return status, r, vcode,

    status = r.status_code
    resp = r.text
    if status == 200:
        if re.search(check_point, str(resp)):
            logging.info(num+' '+api_purpose+'成功~【'+str(status)+'】,'+str(resp))
            return status, resp
        else:
            logging.error(num+' '+api_purpose+'检查点匹配失败！！！，【'+str(status)+'】，'+ str(resp))
            return 200, resp
    else:
        logging.error(num+' '+api_purpose+'接口报错！！！，【'+str(status)+'】，'+ str(resp))
        return status, resp.decode('utf-8'), None


def readData(testCaseFile, sheetname):
    testCaseFile = os.path.join(os.getcwd(), testCaseFile)
    if not os.path.exists(testCaseFile):
        logging.error("测试用例文件不存在！")
        sys.exit()
    testCase = xlrd.open_workbook(testCaseFile)
    table = testCase.sheet_by_name(sheet_name=sheetname)
    errorCase = []

    for i in range(1, table.nrows):
        if table.cell(i, 7).value != 'Yes':
            continue
        num = str(int(table.cell(i, 0).value))
        api_purpose = table.cell(i, 1).value
        api_host = str(table.cell(i, 2).value)
        request_url = str(table.cell(i, 3).value)
        request_method = str(table.cell(i, 4).value)
        request_data = table.cell(i, 5).value
        check_point = str(table.cell(i, 6).value)
        status, resp = interfaceTest(num, api_purpose, api_host, request_url, request_method, request_data, check_point)
        if status != 200 or check_point not in resp:
            errorCase.append((num + ' ' + api_purpose, str(status), 'http://'+api_host+request_url, resp))
    return errorCase
