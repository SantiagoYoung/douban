import requests
from lxml import etree
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
headers = {"User-Agent": user_agent}
from pymongo import MongoClient

conn = MongoClient('localhost', 27017)
db = conn.douban


def freeProxyFifth():
    """
    抓取guobanjia http://www.goubanjia.com/free/gngn/index.shtml
    :return:
    """
    url = "http://www.goubanjia.com/free/gngn/index{page}.shtml"
    for page in range(1, 10):
        page_url = url.format(page=page)
        rsp = requests.get(page_url, headers=headers)
        tree = etree.HTML(rsp.content.decode('utf-8'))
        proxy_list = tree.xpath('//td[@class="ip"]')
        # 此网站有隐藏的数字干扰，或抓取到多余的数字或.符号
        # 需要过滤掉<p style="display:none;">的内容
        xpath_str = """.//*[not(contains(@style, 'display: none'))
                            and not(contains(@style, 'display:none'))
                            and not(contains(@class, 'port'))
                            ]/text()
                    """
        for each_proxy in proxy_list:
            # :符号裸放在td下，其他放在div span p中，先分割找出ip，再找port
            ip_addr = ''.join(each_proxy.xpath(xpath_str))
            port = each_proxy.xpath(".//span[contains(@class, 'port')]/text()")[0]
            ip = '{}:{}'.format(ip_addr, port)
            try:
                rsp = requests.get(ip, headers=headers)
            except Exception as e:
                print('fuck')
                pass
            if rsp.status_code == 200:
                print('saving...')
                db.proxy.insert_one({'proxy': ip})

# if __name__ == '__main__':
#     freeProxyFifth()
proxy = []
for pro in db.proxy.find():
    ip = 'http://' + pro['proxy']
    # print(ip)
    proxy.append(ip)

import random
# for i in range(10):
#     rsp = requests.get("https://www.douban.com/tag/", proxies={'http': random.choice(proxy)})
#     print(rsp)
for i in range(len(proxy)):
    print(" ------------------ " + str(i) + "------------------")
    rsp = requests.get('https://www.baidu.com', headers=headers, proxies={'http': random.choice(proxy)})
    print(rsp.status_code)