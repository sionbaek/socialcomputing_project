from bs4 import BeautifulSoup
from time import sleep
import requests
import json
import re
import csv
import os


with open('./get_long_reviews.csv', 'r') as csvfile:
    list_reader=csv.DictReader(csvfile, delimiter=',')
    movie_list=list(list_reader)
    header = list_reader.fieldnames

for movie in movie_list:
    title=movie['영화명']
    url=movie['url']
    page_num=int(movie['page_num'])
    title.replace(":","_")

    # csv로 저장
    with open('./longreview_top100_{}.csv'.format(title), 'w', encoding='utf8') as csvfile:
        fieldnames=["score", "title", "review", "time"]+header
        writer=csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

    result=list()
    for i in range(1, page_num+1):
        page_url=url+"&page="+str(page_num)
        r=requests.get(page_url)
        soup=BeautifulSoup(r.text, 'html.parser')

        review_list=soup.select('.rvw_list_area > li > a')
        print(url)
        for review in review_list:
            xx=review['onclick'].split(';')[1]
            review_no=int(re.search('\d+', xx)[0])
            print(review_no)
            print(url)
            movie_no=re.search('code\=\d+',url)[0]
            print(movie_no)
            review_url="https://movie.naver.com/movie/bi/mi/reviewread.nhn?nid="+str(review_no)+"&"+movie_no

            rev=requests.get(review_url)
            rev_soup=BeautifulSoup(rev.text, 'html.parser')

            try:
                score=rev_soup.select(".review > .top_behavior > .star_score > em")[0].text
                title=rev_soup.select(".review > .top_behavior > .h_lst_tx")[0].text
                review=rev_soup.select(".review > .user_tx_area")[0].text
                re_time=rev_soup.select(".review > .top_behavior > .wrt_date")[0].text

                print("score: {}, title: {}, time:{}".format(score, title, re_time))
                result_dict={'score':score, 'title':title, 'review':review, 'time':re_time}
                for info in header:
                    result_dict[info]=movie[info]
                result.append(result_dict)

            except:
                print("no star score")

        if i%10==0 or i==page_num:
            with open('./longreview_top100_{}.csv'.format(title), 'a', encoding='utf8') as csvfile:
                fieldnames=["score", "title", "review", "time"]+header
                writer=csv.DictWriter(csvfile, fieldnames=fieldnames)
                for l in range(len(result)):
                    writer.writerow(result[l])
            result=list()
