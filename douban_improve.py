import requests
from lxml import etree
from pymongo import MongoClient
from urllib.parse import quote
import random
import time

conn = MongoClient('localhost', 27017)
db = conn.douban
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}
user_agent = ["Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)",
"Mozilla/4.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)",
"Mozilla/1.22 (compatible; MSIE 10.0; Windows 3.1)",
"Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))",
"Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7)",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 4.0; InfoPath.3; MS-RTC LM 8; .NET4.0C; .NET4.0E)",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 4.0; Tablet PC 2.0; InfoPath.3; .NET4.0C; .NET4.0E)",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; chromeframe/11.0.696.57)",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0) chromeframe/10.0.648.205",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; chromeframe/11.0.696.57)",
"Mozilla/5.0 ( ; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
"Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 5.1; Trident/5.0)"]

UserAgent = []
for i in user_agent:
    UserAgent.append({'User-Agent': i})


proxy = []
for pro in db.proxy.find():
    ip = 'http://' + pro['proxy']
    proxy.append(ip)

class DouBan:
    def __init__(self):
        self.tags_url = 'https://www.douban.com/tag/'

    def get_tags(self):
        response = requests.get(self.tags_url, headers=random.choice(UserAgent), proxies={'http:': random.choice(proxy)})
        tags_page = etree.HTML(response.content.decode('utf-8'))
        tags = tags_page.xpath('//ul[@class="topic-list"]/li')
        for tag in tags:
            tag_name = tag.getchildren()[0].text
            tag_url = tag.getchildren()[0].attrib['href']
            db.tags.insert_one({'tag': tag_name, 'url': tag_url})

    def get_other_tags(self):
        for tag in db.tags.find():
            url = tag['url']
            response = requests.get(url, headers=random.choice(UserAgent), proxies={'http:': random.choice(proxy)})
            html = etree.HTML(response.content.decode('utf-8'))
            tags = html.xpath('//div[@class="topic-list"]//li')
            for tag in tags:
                tag_name = tag.getchildren()[0].text
                tag_url = tag.getchildren()[0].attrib['href']
                db.tags.insert_one({'tag': tag_name, 'url': tag_url})
            time.sleep(30)

    def get_movies(self):
        for tag in db.tags.find():
            tag_name = tag['tag']
            tag_name = quote(tag_name)
            for i in range(0, 600, 15):
                movie = 'https://www.douban.com/tag/{}/movie?start={}'.format(tag_name, i)
                rsp = requests.get(movie, headers=random.choice(UserAgent), proxies={'http:': random.choice(proxy)})
                html = etree.HTML(rsp.content.decode('utf-8'))
                dl_node = html.xpath('//div[@class="mod movie-list"]/dl')
                if dl_node:
                    for dl in dl_node:
                        img_location = dl.find("./dt/a/img").attrib['src']
                        name = dl.find("./dd/a").text.strip()
                        detail_url = dl.find("./dd/a").attrib['href']
                        information = dl.find("./dd/div[@class='desc']").text.strip()
                        rate_num = dl.find("./dd/div[@class='rating']")
                        if rate_num:
                            rate_num = rate_num.getchildren()[1].text
                        else:
                            rate_num = '0.0'
                        db.movies.insert_one({'name': name,
                                              'img': img_location,
                                              'detail_url': detail_url,
                                              'information': information,
                                              'rate_num': rate_num})
                time.sleep(30)

print("starting.....")
spider = DouBan()
spider.get_tags()
spider.get_other_tags()
spider.get_movies()
print("spider over")
