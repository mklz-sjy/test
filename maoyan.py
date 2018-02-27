import requests
import re
from requests.exceptions import RequestException

def get_one_page(url):
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern=re.compile('<dd>.*?title="(.*?)".*?src="(.*?)".*?</dd>',re.S)
    items=re.findall(pattern,html)
    print(type(items))
    for item in items:
        yield{
            'name':item[0],
            'image':item[1]

        }

def main(offset):
    url="http://maoyan.com/board/4?offset="+str(offset)
    html=get_one_page(url)
    for item in parse_one_page(html):
        print(item)

if __name__ == '__main__':
    for i in range(10):
        main(i*10)