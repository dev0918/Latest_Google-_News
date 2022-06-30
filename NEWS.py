from bs4 import BeautifulSoup
import requests, urllib.parse, lxml
import pandas as pd
import os


def scrape(r):
    soup = BeautifulSoup(r,'html.parser')
    details = soup.findAll(class_ = "SbNwzf eeoZZ")
    data = {"Article":[],"Source":[],"Time":[],"Website":[]}
    raw_h4 = soup.findAll('h4')
    raw_h3 = soup.findAll('h3')
    h3,h4,link_h3,link_h4,link,final,count_h3,count_h4 = [],[],[],[],[],[],0,0
    for i in range(len(raw_h3)):
        h3.append(raw_h3[i].text)
        link_h3.append(f"https://news.google.com{raw_h3[i].findAll('a')[0]['href'][1:]}")
    for i in range(len(raw_h4)):
        h4.append(raw_h4[i].text)
        link_h4.append(f"https://news.google.com{raw_h4[i].findAll('a')[0]['href'][1:]}")      
    source = [i.text for i in soup.findAll(class_='SVJrMe')]
    
    for i in range(len(source)):
        if(i%6==0):
            final.append(h3[count_h3])
            link.append(link_h3[count_h3])
            count_h3+=1
        else:
            final.append(h4[count_h4])
            link.append(link_h4[count_h4])
            count_h4+=1
    temp = []
    time = []
    for i in source:
        for idx,j in enumerate(i):
            if(j.isnumeric()):
                break
        temp.append(i[:idx])
        time.append(i[idx:])
    data = {"NEWS" : final, "SOURCE" : temp,'TIME':time,'LINK':link}
    return data

for i in range(1):
    r= requests.get("https://news.google.com/topstories?hl=en-IN&gl=IN&ceid=IN:en")
    df = pd.DataFrame(scrape(r.text))
    if(os.path.isfile("news__.csv")):
        df.to_csv('news__.csv', mode='a', index=False, header=False)
    else:
        df.to_csv('news__.csv',index=False)
    print("Done")
