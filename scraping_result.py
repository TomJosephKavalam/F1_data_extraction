from bs4 import BeautifulSoup 
import requests
import pandas as pd
import re

def scrap_results(url, venue, year):
    html_content=requests.get(url).text
    soup=BeautifulSoup(html_content, 'lxml')
    if int(year)<2005:
        table = soup.find_all('fieldset', attrs={'class':'block'})[2]
    else:
        table = soup.find_all('fieldset', attrs={'class':'block'})[3]
    body = table.find_all("tr")
    head = body[0]
    body_rows = body[1:]
    len(body_rows)

    headings = []
    for item in head.find_all("th"):
        item = (item.text).rstrip("\n")
        headings.append(item)
    if '' in headings:
        headings.remove('')
    all_rows=[]

    for row_num in range(len(body_rows)):
        row=[]
        for row_item in body_rows[row_num].find_all("td"):
            row.append(re.sub("(\xa0)|(\n)|,","",row_item.text))
            if row[0]=='':
                row[0]='DNF'
            while '' in row:
                row.remove('')
        all_rows.append(row)
    df = pd.DataFrame(data=all_rows,columns=headings)
    df.to_csv('Data/'+year+'/'+venue+'.csv', index=False)
