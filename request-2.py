import pandas as pd
import requests
from bs4 import BeautifulSoup
import pathlib



# Input parameters
form_name = input("please enter form number here: ")
min_year = input("please enter the minimum year here: ")
max_year = input("please enter the maximum year here: ")

def irs_form(form_name, min_year, max_year):

    modi_form_name = form_name.replace(' ', '+')

    url = f'https://apps.irs.gov/app/picklist/list/priorFormPublication.html?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow=0&criteria=formNumber&value={modi_form_name}&isDescending=false'

    df = pd.read_html(url)[3]


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

    df = df[df['Product Number'] == form_name]

    df = df[df['Revision Date'].astype(str).between(min_year, max_year, inclusive=True)]
    # df = df[filtered_df]
    return df['Link'].tolist()
print(irs_form(form_name, min_year, max_year))

def download_links(links_list):
    for link in links_list:
        r = requests.get(link)
        pathlib.Path(f'/{form_name}').mkdir(exist_ok=True)
        open('{form_name}-year', 'wb').write(r.content)