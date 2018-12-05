from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import requests
import json
import re
from selenium.common.exceptions import NoSuchElementException
import csv
import os

header = {'User-Agent': ''}

options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36")
# options.add_argument('--incognito')
# prefs = {"profile.default_content_settings.popups": 0, "download.default_directory" : "/movie_revenue_data"}
# options.add_experimental_option("prefs",prefs)

# d = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=options)
d = webdriver.Chrome(executable_path='./chromedriver.exe')
d.implicitly_wait(3)

month=[31,28,31,30,31,30,31,31,30,31,30]

for i in range(1, 12):
    for j in range(1, month[i-1]+1):
        sleep(1)
        mon = "0"+str(i) if i<10 else str(i)
        date = "0"+str(j) if j<10 else str(j)
        full_date='2018-'+mon+'-'+date
        url='http://www.kobis.or.kr/kobis/business/stat/boxs/findDailyBoxOfficeList.do?loadEnd=0&searchType=search&sSearchFrom='+full_date+'&sSearchTo='+full_date+'&sMultiMovieYn=N&sRepNationCd=&sWideAreaCd='
        d.get(url)

        excel_xpath='//*[@class="btn_type01"][1]'
        d.find_element_by_xpath(excel_xpath).click()

        print(full_date)
        alert = d.switch_to.alert
        alert.accept()
