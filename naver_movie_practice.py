from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import requests
import json
import re
from selenium.common.exceptions import NoSuchElementException,TimeoutException
import csv
import os


#WINDOWS OS
header = {'User-Agent': ''}

options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36")
# options.add_argument('--incognito')

d = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=options)
# d=webdriver.Chrome(executable_path='./chromedriver', chrome_options=options) #MAC OS인 경우 이걸로 하세요, 윗줄 주석 처리
# d = webdriver.Chrome(executable_path='./chromedriver.exe')
d.implicitly_wait(3)

with open('./popularmovie_2015-2017.csv', 'r') as csvfile:
    list_reader=csv.DictReader(csvfile, delimiter=',')
    header = list_reader.fieldnames
    movie_list=list(list_reader)

print(header)
print(movie_list)

d.get('https://movie.naver.com/')

for movie in movie_list:
    title=movie['영화명']
    genre=movie['장르']

    movie_input=d.find_element_by_xpath('//*[@id="ipt_tx_srch"]')
    d.execute_script('''
        var movie_input=arguments[0];
        var value=arguments[1];
        movie_input.value=value;
        ''', movie_input, title)
    d.find_element_by_xpath('//*[@class="btn_srch"]').click()
    sleep(2)
    d.find_element_by_xpath('//*[@class="search_list_1"][1]/li[1]/p/a').click()
    sleep(3)


# d.executeScript("d.find_element_by_xpath('//*[@id=\"ipt_tx_srch\"]').setAttribute('value', 'new value for element')")
