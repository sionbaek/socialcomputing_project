# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 17:47:55 2018

@author: Sion
"""

import os
# os.chdir("C:\GitHub\socialcomputing_project")
from bs4 import BeautifulSoup
import urllib
import urllib.request as res
import pandas as pd

# get url 
def get_url_by_name(movie_name): 
    base = "https://www.imdb.com/find?ref_=nv_sr_fn&" 
    rest = "&s=all"
    values = {"q": movie_name} #section, "term": term}
    params = urllib.parse.urlencode(values)
    url = base + params + rest 
    return url 

filename = 'popularmovie_2015-2017(global).csv'
data = pd.read_csv(filename)
movie_names = data["Title"]

review_pages = [] # urls later used for selenium crawling 
for movie_name in movie_names: # search by movie name 
    print(movie_name)
    url = get_url_by_name(movie_name) 
    req = res.urlopen(url)
    soup = BeautifulSoup(req,'html.parser')
    sections = soup.find_all('div',{'class':'findSection'})
    for section in sections:
        if section.find("h3").text == 'Titles' :
            tds = section.find_all("td",{"class":"result_text"})
            href = tds[0].find("a")["href"]
        else:
            pass 
    base = "https://www.imdb.com" 
    page_url = base + href # get closest result 
    
    req2 = res.urlopen(page_url) # go to movie_page 
    soup = BeautifulSoup(req2,'html.parser')
    href2 = soup.find_all('a',{'class':'quicklink'})[2]['href']
    review_page = base + href2 # get user_review link 
    req3 = res.urlopen(review_page)
    if req3:
        print(movie_name, "OK!")
        review_pages.append(review_page)
        print(len(review_pages))

with open("popular_movie(global)_url_list.txt","w+",encoding="utf=8") as f:
    for title,elem in zip(movie_names,review_pages):
        f.write(title)
        f.write(" /// " )
        f.write(elem)
        f.write('\n')
    f.close()

