import requests
import csv
import re
import json
from multiprocessing import Pool#进程池开启多进程
from requests.exceptions import RequestException

def get_one_page(url):
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response
        return None
    except RequestException:
        return None

def parse(html):
    text=html.json()
    for m in range(len(text['data']['cards'])):
        try:
            items = text['data']['cards'][m]
            pattern=re.compile('.*?a>(.*?)<span.*?',re.S)
            zhengwen=re.findall(pattern,items['mblog']['text'])
            yield {
            '时间':items['mblog']['created_at'],
            '话题':items['mblog']['page_info']['page_title'],
            '发送手机': items['mblog']['source'],
            '转发量': str(items['mblog']['reposts_count']),
            '评论量': str(items['mblog']['comments_count']),
            '点赞量': str(items['mblog']['attitudes_count']),
            '正文':items['mblog']['text']
        }
        except KeyError:
            return None


def write_to_file(content):#将解析的数据写入文件
    for i in range(len(list(content.values()))):
        with open('result.txt','a',encoding='utf-8')as f:#参数a是文件以追加形式写入
            f.write(list(content.values())[i]+',')
            f.close()
    with open('result.txt', 'a', encoding='utf-8')as f:  # 参数a是文件以追加形式写入
        f.write('\n')
        f.close()



def main(offset):
    url='https://m.weibo.cn/api/container/getIndex?uid=2679060797&luicode=10000011&lfid=100103type%3D1%26q%3D%E9%9D%92%E6%98%A5%E4%B8%9C%E7%A7%A6&featurecode=20000320&type=uid&value=2679060797&containerid=1076032679060797&page='+str(offset)
    html = get_one_page(url)
    for item in parse(html):
        print(list(item.values()))
        write_to_file(item)



if __name__ == '__main__':
    with open('result.txt', 'a', encoding='utf-8')as f:  # 参数a是文件以追加形式写入
        f.write('时间,话题,发送手机,转发量,评论量,点赞量,正文' + '\n')
    for i in range(100):
        main(i)