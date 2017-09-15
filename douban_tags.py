import requests
from lxml import etree
from pymongo import MongoClient
from urllib.parse import quote

conn = MongoClient('localhost', 27017)
db = conn.douban
tags_url = 'https://www.douban.com/tag/'
headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'}
rsp = requests.get('https://www.douban.com/tag/', headers=headers)


tag_page = etree.HTML(rsp.content.decode('utf-8'))
tags = tag_page.xpath('//ul[@class="topic-list"]/li')
for t in tags:
    tag_name = t.getchildren()[0].text
    tag_url = t.getchildren()[0].attrib['href']
    db.tags.insert_one({'tag': tag_name, 'url': tag_url})

tag = db.tags.find_one({'tag': '香港'})
url = tag['url']
print(url)
rsp = requests.get(url, headers=headers)
html = etree.HTML(rsp.content.decode('utf-8'))
tags = html.xpath('//div[@class="topic-list"]//li')
for tag in tags:
    tag_name = tag.getchildren()[0].text
    tag_url = tag.getchildren()[0].attrib['href']
    db.tags.insert_one({'tag': tag_name, 'url': tag_url})

tag_name = tag['tag']
tag_name = quote(tag_name)
for i in range(0, 600, 15):
    movie = 'https://www.douban.com/tag/{}/movie?start={}'.format(tag_name, i)
    print(movie)
    rsp = requests.get(movie, headers=headers)
    html = etree.HTML(rsp.content.decode('utf-8'))
    dl_node = html.xpath('//div[@class="mod movie-list"]/dl')
    if dl_node:
        for dl in dl_node:
            img_location = dl.find("./dt/a/img").attrib['src']
            detail_url = dl.find("./dd/a").attrib['href']
            information = dl.find("./dd/div[@class='desc']").text.strip()
            rate_num = dl.find("./dd/div[@class='rating']")
            if rate_num:
                rate_num = rate_num.getchildren()[1].text
            else:
                rate_num = '0.0'
            db.movies.insert_one({'img': img_location, 'detail_url': detail_url,
                                    'information': information, 'rate_num': rate_num})


