import requests
from lxml import etree
from pymongo import MongoClient
from urllib.parse import quote
import random

conn = MongoClient('localhost', 27017)
db = conn.douban
user_agent =[{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}]

UserAgent = []
for i in user_agent:
    UserAgent.append(i)
proxy = []

for pro in db.proxy.find():
    ip = 'http://' + pro['proxy']
    proxy.append(ip)



class Books:

    def __init__(self):
        self.tag_url = "https://book.douban.com/tag/?view=cloud"

    def get_html(self, url):
        rsp = requests.get(url, headers=random.choice(UserAgent), proxies={'http': random.choice(proxy)})
        html = etree.HTML(rsp.content.decode('utf-8'))
        return html

    def get_tags(self):
        html = self.get_html(self.tag_url)
        tags = html.xpath("//table[@class='tagCol']//td/a/text()")
        for tag in tags:
            print(tag)
            db.booktags.insert_one({'tag_name': tag})

book_url = "https://book.douban.com/tag/{book}?start={number}&type=T"

book_tag = db.booktags.find_one({'tag_name': '日本'})
print(book_tag['tag_name'])
book_url = book_url.format(book=quote(book_tag['tag_name']), number=0)
print(book_url)

rsp = requests.get(book_url, headers=random.choice(UserAgent), proxies={'http': random.choice(proxy)})
html = etree.HTML(rsp.content.decode('utf-8'))
book_url = html.xpath("//li[@class='subject-item']/div[@class='pic']/a/@href")[0]
book_img = html.xpath("//li[@class='subject-item']/div[@class='pic']/a/img/@src")[0]
book_title = html.xpath("//li[@class='subject-item']/div[@class='info']/h2/a/text()")[0].strip()
book_pub = html.xpath("//li[@class='subject-item']/div[@class='info']/div[@class='pub']/text()")[0].strip()
book_info = html.xpath("//li[@class='subject-item']/div[@class='info']/p/text()")[0].strip()
rate = html.xpath("//span[@class='rating_nums']/text()")[0].strip()
comment_num = html.xpath("//li[@class='subject-item']//span[@class='pl']/text()")[0].strip()
import re
comment_num = re.search(r'(\d+)', comment_num).group()
print(book_url, book_img, book_title, book_pub, book_info, rate, comment_num)