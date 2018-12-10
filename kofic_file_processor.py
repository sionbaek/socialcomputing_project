# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 21:01:03 2018

@author: Sion
"""

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re 

def main(file): #process given html file into csv 
    f = open(file,"r",encoding="utf-8")
    b = f.read()
    soup = BeautifulSoup(b,"html.parser")
    date = soup.find("h4").text
    date = re.sub("년|월|일","",date)
    date = date.replace(" ","")
    trs = soup.find_all("tr") # each movies 
    cols = trs[0].find_all("th")
    headers = [t.text.strip() for t in cols]
    headers.insert(0,"날짜")
    trs = trs[1:-1]
    data = [] 
    for elem in trs:
        tds = elem.find_all("td")
        result = [t.text for t in tds]
        result = [t.strip() for t in result]
        result.insert(0,date)
        data.append(result)
                                                                
    dat = [np.asarray(t) for t in data]
    df = pd.DataFrame(data=dat,columns=headers)
    file_name = date[:8]+".csv" 
    os.chdir("C:\GitHub\socialcomputing_project\\processed")
    df.to_csv(file_name,encoding="utf-8",index=False)
    os.chdir("C:\GitHub\socialcomputing_project\\file")

# file = "a.xls"
# main(file)

import os 
os.chdir("C:\GitHub\socialcomputing_project\\file")
i = 0
for filename in os.listdir(os.getcwd()):  
    print(filename, i)
    i = i+1 
    main(filename)


    
