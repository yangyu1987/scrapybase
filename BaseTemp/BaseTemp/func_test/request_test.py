# -*-coding:utf-8 -*-
import requests
# from selenium import webdriver
from BaseTemp.tools.proxy_ip import get_ip
# selenium
# browse = webdriver.Firefox(executable_path='geckodriver')
# browse.get('https://www.chahaoba.com/index.php?title=%E5%88%86%E7%B1%BB:%E9%AA%97%E5%AD%90%E5%8F%B7%E7%A0%81&amp%3Bpagefrom=%2B02227393016%EF%BC%9B%2B37911183&pagefrom=%2B223056258#mw-pages')
# print(browse.page_source)

# proxy
proxies = {
  "https": get_ip(),
}
print(get_ip())
res = requests.get("https://www.baidu.com", proxies=proxies)
print(res.text)
