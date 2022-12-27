from scraping_result import *

import pandas as pd
from bs4 import BeautifulSoup 
import requests
import re


def scrap_race(url, year):
    html_content=requests.get(url).text
    soup=BeautifulSoup(html_content, 'lxml')
    body=soup.find_all('fieldset', attrs={'class':'block'})[2].find_all('tr')
    head=body[0]
    body_rows=body[1:]
    headings = []
    for item in head.find_all("th"):
        item = (item.text).rstrip("\n")
        headings.append(item)
    all_rows=[]

    for row_num in range(len(body_rows)):
        row=[]
        url_prix=body_rows[row_num].find_all('td')[2].find('a').get('href')
        for row_item in body_rows[row_num].find_all("td"):
            row.append(re.sub("(\xa0)|(\n)|,","",row_item.text))
        row.pop(4)
        all_rows.append(row)
        print(row[2]+' going on.....')
        scrap_results(url_prix, row[2], year)

    df = pd.DataFrame(data=all_rows,columns=headings)
    df.to_csv('Data/'+year+'/'+year+'.csv', index=False)


