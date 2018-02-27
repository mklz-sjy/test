#猫眼热映口碑榜
#抓包分析直接传来原文件，因此正则表达式直接做一类的提取
import requests
from requests.exceptions import RequestException
import re
import json


def getdata(url):#获取网页原数据
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
    except RequestException:
        return print('RequestException')

def parseurl(text):#解析原数据
    pattern=re.compile('<dd>.*?"\stitle="(.*?)"\sclass=.*?star">(.*?)</p>.*?/dd>',re.S)#设置匹配模式，re.S表示.可指代换行符 .*?非贪婪匹配
    items=re.findall(pattern,text)#提取所有满足条件的字符
    for item in items:#字典形式存储
        yield{
            'name':re.sub('\s','',item[0]),#此处若单个item时，用item即可，若用item[0]只提取其中电影名首字母
            'star':re.sub('\s','',item[1])
        }

def write_to_file(content):#将解析的数据写入文件
    with open('result.txt','a',encoding='utf-8')as f:#参数a是文件以追加形式写入
        f.write(json.dumps(content)+'\n')
        f.close()


def foremain():#主函数
    url='http://maoyan.com/board/7'
    text=getdata(url)
    for item in parseurl(text):
        print(item)
        write_to_file(item)

if __name__=='__main__':#执行函数
    foremain()