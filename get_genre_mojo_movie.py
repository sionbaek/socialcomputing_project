# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 02:45:11 2018

@author: Sion
"""

from bs4 import BeautifulSoup
import urllib.request as res
import csv
import pandas as pd
import numpy as np


def get_genre(url):
    data = res.urlopen(url)
    soup = BeautifulSoup(data,"html.parser")
    tds = soup.find_all("td")
    td = tds[4]
    bs = td.find_all("b")
    b = bs[4].text
    return(b)

# url = "https://www.boxofficemojo.com/movies/?id=theincredibles2.htm"
url = "https://www.boxofficemojo.com/movies/?id=pixar2015.htm"
url = "https://www.boxofficemojo.com/movies/?id=marvel2017b.htm"
url = "https://www.boxofficemojo.com/movies/?id=jurassicworldsequel.htm"

get_genre(url)

df=pd.read_csv('mojo_movie.csv')

genre_list=list()

i=0
for item in df['link']:
    i+=1
    if item != None:
        try:
            genre=get_genre("https://www.boxofficemojo.com"+str(item))
            print(str(i)+" : "+genre)
            genre_list.append(genre)
        except:
            print("genre error")
    else:
        genre_list.append(None)

genre_column=pd.Series(genre_list)

df['genre']=genre_column.values

print(df)

df.to_csv('mojo_mov.csv', index=False)
