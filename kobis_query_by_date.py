from selenium import webdriver
from time import sleep
import pandas as pd
import os
import re

d = webdriver.Chrome(executable_path='./chromedriver.exe')

def query(date): #yyyy-mm-dd 
    header = {'User-Agent': ''}
    options = webdriver.ChromeOptions()
    d.implicitly_wait(3)
    url='http://www.kobis.or.kr/kobis/business/stat/boxs/findDailyBoxOfficeList.do?loadEnd=0&searchType=search&sSearchFrom='+date+'&sSearchTo='+date+'&sMultiMovieYn=N&sRepNationCd=&sWideAreaCd='
    d.get(url)

    excel_xpath='//*[@class="btn_type01"][1]'
    d.find_element_by_xpath(excel_xpath).click()

    print(date)
    alert = d.switch_to.alert
    alert.accept()
 
os.chdir("C:\\GitHub\\socialcomputing_project")
f = pd.read_csv("popularmovie_2015-2017.csv")
titles = list(f["영화명"])
dates = f["개봉일"]

seven = [t for t in dates if t[:4] == '2017'] 
six = [t for t in dates if t[:4] == '2016']
five = [t for t in dates if t[:4] == '2015']

for date in five:
    query(date)


os.chdir(".\processed")
actors = [] 
for filename in os.listdir(os.getcwd()):  
    tmp = pd.read_csv(filename)
    for item in tmp.iterrows():
        if item[1]["영화명"] in title:
            temp = (item[1]["영화명"],item[1]["배우"])
            actors.append(temp)
actors = list(set(actors))
actors = [t for t in actors if type(t[1]) == str]
f = open("actors_list.txt","w+",encoding="utf-8")
for elem in actors:
    f.write(" : ".join(elem))
    f.write("\n")




# usage query('2017-10-20')

    

