#爬取豆瓣2017年度好书榜

import requests
from requests.exceptions import RequestException
from selenium import webdriver

def gethtml(url):#网页原数据获取
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
    except RequestException:
        return print('erro2')

def foremain(offset):#主函数构造url
    url='https://book.doubn.com'
    text=gethtml(url)


if __name__=='__main__':#执行函数
    browser = webdriver.Chrome()
    browser.get('https://www.taobao.com')
    print(browser.page_source)
    browser.close()
    for i in range(46):
        foremain(i)