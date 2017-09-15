import requests
from lxml import etree
from pymongo import MongoClient

conn = MongoClient('localhost', 27017)
db = conn.douban
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
headers = {"User-Agent": user_agent}

rsp = requests.get("http://www.xicidaili.com/nn/1", headers=headers)
html = etree.HTML(rsp.content.decode('utf-8'))
ip_list = html.xpath("//tr[@class='odd']")
# print(ip_list[0].getchildren()[1].text)
# print(ip_list[0].getchildren()[2].text)
# ip = 'http://' + ip_list[0].getchildren()[1].text + ':' + ip_list[0].getchildren()[2].text
# print(ip)
for ip in ip_list:
    ip = 'http://' + ip.getchildren()[1].text + ":" + ip.getchildren()[2].text
    print(ip)
    rsp = requests.get(ip, headers=headers)
    if rsp.status_code == '200':
        db.proxy.insert_one({'proxy': ip})
        print('ok')


# url = "http://www.kuaidaili.com/free/inha/{}/"
# for i in range(20):
#     url.format(i)
#     print(url)
#     rsp = requests.get(url, headers=headers)
#     html = etree.HTML(rsp.content)
#     ip_list = html.xpath("//tr")
# url = "http://www.kuaidaili.com/free/inha/2/"
# from selenium import webdriver
# driver = webdriver.PhantomJS()
# driver.get(url)
# ip_list = driver.find_elements_by_xpath("//div[@id='list']//tbody/tr")
# print(ip_list)
# for i in ip_list:
#     print(i + " 000000000000000000000")
#     td = i.find_element_by_xpath(".//td")
#     print(td)




# rsp = requests.get(url, headers=headers)
# html = etree.HTML(rsp.content.decode('utf-8'))
# ip_list = html.xpath("//div[@id='list']//tbody//tr")
