import pandas as pd
import json
import requests
from bs4 import BeautifulSoup

formName = input("Enter form name here: ").replace(' ', '+')


url = f'https://apps.irs.gov/app/picklist/list/priorFormPublication.html?value={formName}&criteria=formNumber&submitSearch=Find'

df = pd.read_html(url)[3]
# print(df[3])
# df_json = df[3] 
# .to_json(f'{formName}.json')
# print(df_json)
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find_all('table')[3]

links = []
for tr in table.findAll("tr"):
    trs = tr.findAll("td")
    for each in trs:
        try:
            link = each.find('a')['href']
            links.append(link)
        except:
            pass

df['Link'] = links
print(df)
df_json = df.to_json(f'{formName}.json')