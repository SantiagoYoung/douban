import requests
from PIL import Image, ImageEnhance, ImageFilter
from bs4 import BeautifulSoup
from selenium import webdriver
import pytesseract
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.PhantomJS()
driver.get("http://jwxt.swpu.edu.cn")

driver.save_screenshot("./s.png")
element = driver.find_element_by_id("vchart")

account = driver.find_element_by_name("zjh")
passwd = driver.find_element_by_name('mm')
captcha = driver.find_element_by_name("v_yzm")
login = driver.find_element_by_id("btnSure")

location = element.location
left = location['x']
top = location['y'] + 8
right = left + element.size['width']
bottom = top + element.size['height']

im = Image.open("./s.png")
im.show()
code = input("enter the code: ")
# im = im.convert("L")
# for i in range(2):
#     im = im.filter(ImageFilter.MedianFilter)
# im_crop = im.crop((left, top, right, bottom))
# im_crop.save("./vv.png")
# im = Image.open("./vv.png")
# tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
# text = pytesseract.image_to_string(im, config=tessdata_dir_config)
# code = ''
# for i in text:
#     code += i.strip()
print(code)
account.send_keys("1216020110")
passwd.send_keys("864571")
captcha.send_keys(code)
login.send_keys(Keys.ENTER)
time.sleep(2)

current_url = driver.current_url
cookie = [item['name'] + "=" + item['value'] for item in driver.get_cookies()]
cookies = {}
for i in cookie:
    name, value = i.split("=")
    cookies[name] = value
data = {
    "zjh": '1216020110',
    "mm": '864571'
}
rsp = requests.post("http://jwxt.swpu.edu.cn/loginAction.do", data=data, cookies=cookies)
print(rsp.content.decode("gbk"))























