from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import requests
import json
import re
from selenium.common.exceptions import NoSuchElementException
import csv
import os

def get_page_num():
    review_num=d.find_element_by_xpath('//*[@class="score_total"]/strong/em').text
    review_num=review_num.replace(",","")
    page_num=(int(review_num)//10) + 1

    return page_num

def get_reviews(page_num, released):
    result=list()
    for j in range(1, page_num+1):
        sleep(2)
        page_xpath='//*[@id="pagerTagAnchor'+str(j)+'"]'
        d.find_element_by_xpath(page_xpath).click()

        for i in range(1,11):
            try:
                root_xpath='//*[@class="score_result"]/ul/li['+str(i)+']'
                score_xpath=root_xpath+'/div[@class="star_score"]/em'
                review_xpath=root_xpath+'/div[@class="score_reple"]/p'
                time_xpath=root_xpath+'/div[@class="score_reple"]/dl/dt/em[2]'
                score=d.find_element_by_xpath(score_xpath).text
                review=d.find_element_by_xpath(review_xpath).text
                re_time=d.find_element_by_xpath(time_xpath).text
                print("score: {}, review: {}, time:{}".format(score, review, re_time))
                result.append({'score':score, 'review':review, 'time':re_time, 'released':released})
            except:
                print("no xpath found")
                pass
    return result


#WINDOWS OS
header = {'User-Agent': ''}

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36")
options.add_argument('--incognito')

d = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=options)
# d=webdriver.Chrome(executable_path='./chromedriver', chrome_options=options) #MAC OS인 경우 이걸로 하세요, 윗줄 주석 처리
# d = webdriver.Chrome(executable_path='./chromedriver.exe')
d.implicitly_wait(3)

d.get('https://movie.naver.com/movie/bi/mi/basic.nhn?code=167638') #167638
d.find_element_by_xpath('//*[@class="tab05_off"]').click()

movie_title=d.find_element_by_xpath('//*[@class="mv_info_area"]/div[@class="mv_info"]/h3/a[1]').text
print(movie_title)
movie_title.replace(":", "_")

# 개봉 후 평점 받아오기, 한 페이지에 열 개
# page 내부, 네티즌 댓글 전용 iframe 들어가기
d.switch_to.frame("pointAfterListIframe")
page_num=get_page_num()
result=get_reviews(page_num, True)

#개봉 전 받아오기
d.switch_to.default_content()
d.find_element_by_xpath('//*[@id="beforePointTab"]/a').click()

d.switch_to.frame("pointAfterListIframe")
page_num2=get_page_num()
result2=get_reviews(page_num2, False)

d.quit()

# csv로 저장
with open('./review_{}.csv'.format(movie_title), 'w', encoding='utf8') as csvfile:
    fieldnames=["score", "review", "time", "released"]
    writer=csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for i in range(len(result)):
        writer.writerow(result[i])
    for j in range(len(result2)):
        writer.writerow(result2[j])
