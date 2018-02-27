# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
import json


# 微博内容
class WeiBoWBSpider(scrapy.Spider):

    name = 'weibo_wb_spider'
    allowed_domains = ['weibo.com']


    def __init__(self, task_id=None, object_urls=None, *args, **kwargs):
        super(WeiBoWBSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://m.weibo.cn/p/1005052803301701',
                           'https://m.weibo.cn/u/2189067512']

    def start_requests(self):
        for start_url in self.start_urls:
            containerid = ''
            url_head = 'https://m.weibo.cn/api/container/getIndex?containerid='
            if 'https://m.weibo.cn/p/' in start_url:
                containerid = start_url.replace('https://m.weibo.cn/p/','').replace('100505','107603')
            elif 'https://m.weibo.cn/u/' in start_url:
                containerid = '107603' + start_url.replace('https://m.weibo.cn/u/', '')
            if containerid:
                origin_url = '%s%s'%(url_head,containerid)
                yield Request(origin_url,callback=self.parse)


    def parse(self, response):
        content = json.loads(response.body)
        weibo_info = content.get('cards',[])
        for info in weibo_info:
            if info.get('mblog') and info.get('mblog').get('text'):
                title = (info['mblog']['text']).encode('utf8')
                url = "https://m.weibo.cn/status/%s" % info["mblog"]["mid"]
                time_str = info.get('mblog').get('created_at').encode('utf8')
                picture_urls = ''
                if info.get('mblog').get('page_info'):
                    if info.get('mblog').get('page_info').get('media_info'):
                        picture_urls = info.get('mblog').get('page_info').get('page_pic')['url']
                if not picture_urls:
                    if info.get('mblog').get('pics'):
                        pics = map(lambda x:x.get('url'),info["mblog"]["pics"])
                        picture_urls = ','.join(pics)

                print '======微博内容======'
                print title
                print url
                print time_str
                print picture_urls


