# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 02:45:11 2018

@author: Sion
"""

from bs4 import BeautifulSoup
import urllib.request as res
        
def get_genre(url): 
    data = res.urlopen(url)
    soup = BeautifulSoup(data,"lxml")
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