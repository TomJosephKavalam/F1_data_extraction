from scraping_race import *

import pandas as pd
from bs4 import BeautifulSoup 
import requests
import re
import os

url='https://www.racing-statistics.com/en/seasons'

html_content=requests.get(url).text
soup=BeautifulSoup(html_content, 'lxml')

body=soup.find_all('fieldset', attrs={'class':'block'})[0].find_all('tr')
head=body[0]
body_rows=body[1:]

headings = []
for item in head.find_all("th"):
    item = (item.text).rstrip("\n")
    headings.append(item)

all_rows=[]

for row_num in range(len(body_rows)):
    row=[]
    url_season=body_rows[row_num].find_all('td')[1].find('a').get('href')
    for row_item in body_rows[row_num].find_all("td"):
        row.append(re.sub("(\xa0)|(\n)|,","",row_item.text))
    all_rows.append(row)

all_rows=[]

for row_num in range(len(body_rows)):
    row=[]
    for row_item in body_rows[row_num].find_all("td"):
        row.append(re.sub("(\xa0)|(\n)|,","",row_item.text))
    all_rows.append(row)
    url_season=body_rows[row_num].find_all('td')[1].find('a').get('href')
    newpath = "Data/"+str(row[1])
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    print(row[1]+' going on.....')
    scrap_race(url_season, row[1])

df = pd.DataFrame(data=all_rows,columns=headings)
df.to_csv('History.csv', index=False)  



