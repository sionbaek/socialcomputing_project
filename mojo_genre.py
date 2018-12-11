from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import requests
import json
import re
from selenium.common.exceptions import NoSuchElementException
import csv
import os
#
# with open('./2015_movie.csv', 'r') as csvfile:
#     list_reader=csv.DictReader(csvfile, delimiter=',')
#     movie_list=list(list_reader)
#     header = list_reader.fieldnames
#
# for movie in movie_list:
#     print(movie['link'])
#     page=requests.get('https://www.boxofficemojo.com'+movie['link'])
#
#     soup = BeautifulSoup(page.text, 'html.parser')



page=requests.get('https://www.boxofficemojo.com/movies/?id=starwars7.htm')

soup = BeautifulSoup(page.text, 'html.parser')

# body2=soup.find('div', {'id':'body'})
# body2.find('table[2]/tbody/tr/td/table[1]/tbody/tr/td[2]/table/tbody/tr/td/center/table/tbody/tr[3]/td[1]/b')

# li=body2.find('table[2]/tbody/tr/td/table[1]/tbody/tr/td[2]/table/tbody/tr/td/center/table/tbody/tr[3]/td[1]/b')
x=soup.find('#body > table:nth-child(2) > tbody > tr > td > table:nth-child(1) > tbody > tr > td:nth-child(2) > table > tbody > tr > td > center > table > tbody > tr:nth-child(3) > td:nth-child(1) > b')
print(x)
