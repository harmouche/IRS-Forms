import pandas as pd
import json
import requests
from bs4 import BeautifulSoup

ilist = ['Form W-2', 'Form 1095-C', 'Form 1099-MISC', 'Form W-2 P']


def irs_form(form_name):

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
    new_result = {
    "form_number": df.iloc[1,0],
    "form_title": df.iloc[1,1],
    "min_year": int(df['Revision Date'][df['Revision Date'].idxmin()]),
    "max_year": int(df['Revision Date'][df['Revision Date'].idxmax()])}

    output = json.dumps(new_result)
    return output


def irs_forms(ilist):
    output_list = []
    for element in ilist:
        output_list.append(irs_form(element))
    return output_list
print(irs_forms(ilist))