from urllib.request import urlopen
from bs4 import BeautifulSoup
import pprint
import re
import json
import io

try:
    to_unicode = unicode
except NameError:
    to_unicode = str

soup = BeautifulSoup(urlopen("http://www.hindustantimes.com/world/"),'html.parser').find_all("div",{"id": "scroll-container"})

arr = []
arrr =[]
k = {'world_news':""}
#print(soup)
pp = pprint.PrettyPrinter(indent=4)

#link_more = soup[0].ul.find_all("a",attrs={'href': re.compile("^https://")})

for link in soup[0].ul.find_all("a",attrs={'href': re.compile("^https://")}):
        if(link.get('href') not in arr):
                arr.append(link.get('href'))

pp.pprint(arr)
cnt = 0
for url in arr:
        '''cnt = cnt+1
        if cnt == 24:
                break'''
        paragraph = ""
        soup = BeautifulSoup(urlopen(url),'html.parser').find("span",{"class": "text-dt"})
        added_on = soup.text
        soup = BeautifulSoup(urlopen(url),'html.parser').find("h1",{"itemprop": "headline"})
        title = soup.text;
        soup = BeautifulSoup(urlopen(url),'html.parser').find("img",attrs={'src': re.compile("^https://www.hindustantimes.com/rf/image_size_960x540/HT/p2/")})
        img_link = soup.get('src')
        print(img_link)
        soup = BeautifulSoup(urlopen(url),'html.parser').find_all("div",{"class": "story-details"})
        for para in soup[0].find_all('p'):
                paragraph += para.text
        content = paragraph

        datas = {'header':title,'img_link':img_link,'content':content,'added_on':added_on};
        arrr.append(datas.copy())
        k['world_news']= arrr

        #print(k['world_news'])
with io.open('world_api.json', 'w', encoding='utf8') as outfile:
    str_ = json.dumps(k,
                      indent=4, sort_keys=False,
                      separators=(',', ': '), ensure_ascii=False)
    outfile.write(to_unicode(str_))
