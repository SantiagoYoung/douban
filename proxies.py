import requests
from lxml import etree
from pymongo import MongoClient

conn = MongoClient('localhost', 27017)
db = conn.douban
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
headers = {"User-Agent": user_agent}

for i in range(50):
    url = "http://www.xicidaili.com/nn/{}".format(i)
    rsp = requests.get(url, headers=headers)
    html = etree.HTML(rsp.content.decode('utf-8'))
    ip_list = html.xpath("//tr[@class='odd']")
    for ip in ip_list:
        ip = 'http://' + ip.getchildren()[1].text + ":" + ip.getchildren()[2].text
        print(ip)
        try:
            rsp = requests.get(ip, headers=headers)
            print(rsp.status_code)
            if rsp.status_code == 200:
                db.proxy.insert_one({'proxy': ip})
        except Exception as e:
            print('no')
            pass

