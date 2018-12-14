from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import requests
import json
import re
from selenium.common.exceptions import NoSuchElementException,TimeoutException
import csv
import os

header = {'User-Agent': ''}

options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36")
# options.add_argument('--incognito')

d = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=options)
# d=webdriver.Chrome(executable_path='./chromedriver', chrome_options=options) #MAC OS인 경우 이걸로 하세요, 윗줄 주석 처리
# d = webdriver.Chrome(executable_path='./chromedriver.exe')
d.implicitly_wait(3)


f = open("popular_movie(global)_url_list.txt","r",encoding="utf-8")
b = f.readlines()
title = [t.split(" /// ")[0] for t in b ]
url = [t.split(" /// ")[1] for t in b ]
# genre = [t.split(" /// ")[2] for t in b]

for t, u in zip(title,url):
    print(t)
    t=t.replace(':', '-')
    d.get(u)

    #여러 번 load 하기
    review_num=d.find_element_by_xpath('//*[@class="header"]/div/span').text
    review_num=review_num.replace(' Reviews','')
    review_num=review_num.replace(',','')
    page_num=int(review_num)//25+1
    print(review_num)
    print(page_num)

    for i in range(1, page_num+1):
        sleep(5)
        bt=d.find_element_by_xpath('//*[@id="load-more-trigger"]')
        d.execute_script('''
                var bt=arguments[0];
                bt.click();
                ''', bt)

    sleep(5)

    #review 찾기
    reviews=d.find_elements_by_xpath('//*[@class="review-container"]')
    print(len(reviews))
    # print(reviews)

    with open('./review_genre_{}.csv'.format(t), 'w', encoding='utf8') as csvfile:
        fieldnames=["score", "title", "time", "review"]
        writer=csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    result=list()
    for data in reviews:
        dt=BeautifulSoup(data.get_attribute("innerHTML"),"html.parser")
        try:
            score=data.find_element_by_xpath('.//*[@class="rating-other-user-rating"]/span[1]').text
            title=data.find_element_by_xpath('.//*[@class="title"]').text
            time=data.find_element_by_xpath('.//*[@class="review-date"]').text
            review=dt.find_all('div', {'class':'show-more__control'})[0].text
            print('score:'+score+', title:'+title+', time:'+time)
            result.append({'score':score, 'title':title, 'time':time, 'review':review})
        except:
            print("아아아아악")

        if len(result)>=50:
            with open('./review_{}_{}.csv'.format("genre", t), 'a', encoding='utf8') as csvfile:
                fieldnames=["score", "title", "time", "review"]
                writer=csv.DictWriter(csvfile, fieldnames=fieldnames)
                for l in range(len(result)):
                    writer.writerow(result[l])
            result=list()

    with open('./review_genre_{}.csv'.format(t), 'a', encoding='utf8') as csvfile:
        fieldnames=["score", "title", "time", "review"]
        writer=csv.DictWriter(csvfile, fieldnames=fieldnames)
        for l in range(len(result)):
            writer.writerow(result[l])
