# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 18:18:52 2018

@author: Sion
"""

import os
os.chdir("C:\GitHub\socialcomputing_project")
import re
import pandas as pd 
from ckonlpy.tag import Twitter
from ckonlpy.tag import Postprocessor
twitter = Twitter()
            
f = open("actors_list.txt","r",encoding="utf-8")
b = f.readlines()
temp = [t.split(" : ")[1] for t in b]
actors = [t.split(",") for t in temp]
actors_list = []
for elem in actors:
    actors_list.extend(elem)
actors_list = list(set(actors_list))
twitter.add_dictionary(actors_list,"Noun") # add names of actors as Noun 


f = pd.read_csv("popularmovie_2015-2017.csv")
title = list(f["영화명"])
title = [re.sub(r":|-|,"," ",elem) for elem in title]
ngrams = [] # change in to n-grams
for elem in title:
    temp = twitter.pos(elem)
    temp2 = [t[0] for t in temp]
    ngrams.append((tuple(temp2),'Noun'))
    
postprocessor = Postprocessor(twitter, ngrams = ngrams)
#read_review_data
sentences = ['황정민이 굿바이 싱글에 출연해 큰 호응을 얻었습니다',\
             '겟 아웃은 김혜수가 출연하지 않았습니다'\
             '너무너무 재미있어요! 감동적입니다']

passtags = {'Adjective'}
postprocessor = Postprocessor(twitter, passtags = passtags, ngrams=ngrams)
nouns = [postprocessor.pos(t) for t in sentences]



    


