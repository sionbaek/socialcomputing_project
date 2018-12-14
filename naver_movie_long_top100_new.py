from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import requests
import json
import re
from selenium.common.exceptions import NoSuchElementException,TimeoutException
import csv
import os

def get_longpage_num(movie_link):
    d.get(movie_link)
    data=d.find_element_by_xpath('//*[@class="review"]')
    
    dt=BeautifulSoup(data.get_attribute("innerHTML"), 'html.parser')
    
    good_num=dt.find_all('em',{'class':'num_good'})[0].text
    bad_num=dt.find_all('em',{'class':'num_bad'})[0].text
    
    good_num=good_num.replace('명','')
    good_num=good_num.replace(',','')
    bad_num=bad_num.replace('명','')
    bad_num=bad_num.replace(',','')
    review_num=int(good_num)+int(bad_num)
    print(review_num)
    
    page_num=((int(review_num)-1)//10) + 1
    page_num= page_num if page_num>=1 else 1

    return page_num

def get_longreviews(page_num, header, movie_info, movie_title, review_link):
    # page_num=2
    result=list()
    for j in range(1, page_num+1):
        sleep(2)
        cur_url=review_link+"&page="+str(j)
        d.get(cur_url)

        for i in range(1,11):
            try:
                d.find_element_by_xpath('//*[@class="rvw_list_area"]/li['+str(i)+']/a').click()
                sleep(2)

                root_xpath='//*[@class="review"]'
                header_xpath=root_xpath+'/div[@class="top_behavior"]'

                score_xpath=header_xpath+'/div[@class="star_score"]/em'
                title_xpath=header_xpath+'/strong[@class="h_lst_tx"]'
                review_xpath=root_xpath+'/div[@class="user_tx_area"]'
                time_xpath=header_xpath+'/span[@class="wrt_date"]'

                score=d.find_element_by_xpath(score_xpath).text
                title=d.find_element_by_xpath(title_xpath).text
                review=d.find_element_by_xpath(review_xpath).text
                re_time=d.find_element_by_xpath(time_xpath).text
                print("score: {}, title: {}, review: {}, time:{}".format(score, title, review, re_time))
                result_dict={'score':score, 'title':title, 'review':review, 'time':re_time}
                for info in header:
                    result_dict[info]=movie_info[info]
                result.append(result_dict)
            except:
                print("no xpath found")
                pass
            d.get(cur_url)
            sleep(1)
            
        if j%10==0 or j==page_num:
            with open('./longreview_top100_{}.csv'.format(movie_title), 'a', encoding='utf8') as csvfile:
                fieldnames=["score", "title", "review", "time"]+header
                writer=csv.DictWriter(csvfile, fieldnames=fieldnames)
                for l in range(len(result)):
                    writer.writerow(result[l])
            result=list()



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

with open('./popularmovie_2015-2017_long.csv', 'r') as csvfile:
    list_reader=csv.DictReader(csvfile, delimiter=',')
    movie_list=list(list_reader)
    header = list_reader.fieldnames

d.get('https://movie.naver.com/')

for movie in movie_list:
    title=movie['영화명']

    
    movie_input=d.find_element_by_xpath('//*[@id="ipt_tx_srch"]')
    d.execute_script('''
        var movie_input=arguments[0];
        var value=arguments[1];
        movie_input.value=value;
        ''', movie_input, title)
    d.find_element_by_xpath('//*[@class="btn_srch"]').click()
    sleep(2)
    movie_link=d.find_element_by_xpath('//*[@class="search_list_1"][1]/li[1]/p/a')
    sleep(3)
    review_link=movie_link.get_attribute('href')
    
    page_num=get_longpage_num(review_link)
    
    
    review_link=review_link.replace("basic","review")

    d.get(review_link+"&page=1")

    movie_title=d.find_element_by_xpath('//*[@class="mv_info_area"]/div[@class="mv_info"]/h3/a[1]').text
    print(movie_title)
    movie_title=movie_title.replace(":", "_")

    # csv로 저장
    with open('./longreview_top100_{}.csv'.format(movie_title), 'w', encoding='utf8') as csvfile:
        fieldnames=["score", "title", "review", "time"]+header
        writer=csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        
    
    get_longreviews(page_num, header, movie, movie_title, review_link)

    # 기본으로 되돌리기
    d.switch_to.default_content()

    

# d.get('https://movie.naver.com/movie/bi/mi/basic.nhn?code=167638') #167638


d.quit()
