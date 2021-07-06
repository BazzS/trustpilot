import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.trustpilot.com/categories/financial_consultant'
r = requests.get(url,headers={
"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
})

soup = BeautifulSoup(r.text,'html.parser')
last_page = int(soup.find('a',{'name':'pagination-button-last'}).text)
count = 1
result = []

for page in range(1,last_page+1):
    ends = soup.find('span',{'class':'styles_resultsText__veT7A'})
    if ends == None:
        url_page = f'https://www.trustpilot.com/categories/financial_consultant?page={page}'
        r = requests.get(url_page,headers={
        "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        })
        soup = BeautifulSoup(r.text,'html.parser')
        items = soup.find('div',{'class':'styles_businessUnitCardsContainer__1ggaO'})
        urls = items.find_all('a',href=True)
        for i in urls:
            newurl = 'https://www.trustpilot.com' + i['href']
            newR = requests.get(newurl,headers={
            "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
            })
            soup2 = BeautifulSoup(newR.text,'html.parser')
            title = soup2.title.string
            beauty_title = title[:title.find('Reviews')]
            rating = soup2.find('p',{'class':'header_trustscore'}).text
            domen_begin = soup2.find('span',{'class':'smart-ellipsis__prefix'}).text
            domen_end = soup2.find('span',{'class':'smart-ellipsis__suffix'}).text
            domen = domen_begin + domen_end
            result.append({
                "Название" : beauty_title,
                "Рейтинг" : rating,
                "Домен" : domen,
                })
            print(count, beauty_title, rating, domen)
            count += 1
    else:
        break

with open('result.json','a') as file:
    json.dump(result, file, indent = 2, ensure_ascii = False)
