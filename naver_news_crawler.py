# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 13:23:32 2018

@author: Sion
"""

import urllib.request
from bs4 import BeautifulSoup,NavigableString
import numpy as np
import pandas as pd
import re 

url = "https://search.naver.com/search.naver?&where=news&query=%EC%99%84%EB%B2%BD%ED%95%9C%2B%ED%83%80%EC%9D%B8&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&cluster_rank=15&start="
start = 1


# collectiong url 
urls = [] 
while start < 502: #num of page  
    res = urllib.request.urlopen(url)
    soup = BeautifulSoup(res,"html.parser")
    content = soup.find_all("a", class_ ="_sp_each_url")    
    temp = [t["href"] for t in content]
    urls.extend(temp)
    start += 10
    url = url + str(start) 

# function for collecting contents 
def contents_collector(url):
    try:
        res = urllib.request.urlopen(url)
        soup = BeautifulSoup(res,"html.parser")
    except:
        pass
    if soup:
        content = soup.find_all("div", class_ ="article_body font1 size3")    
        inner_text = [element for element in content[0] if isinstance(element, NavigableString)]
        inner_text = inner_text[:-1] # get rid of 무단전재배포...저작권 
        text = [t.strip() for t in inner_text] # strip whitespace 
        text = [t for t in text if len(t) >1]
    else:
        text = [] 
    return text
    
contents = [] 
for url in urls:
    contents.append(contents_collector(url))


