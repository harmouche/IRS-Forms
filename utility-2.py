import pandas as pd
import requests
from bs4 import BeautifulSoup
import os



# Input parameters
form_name = input("please enter form number here: ")
min_year = input("please enter the minimum year here: ")
max_year = input("please enter the maximum year here: ")

# Takes input and retruns a list of files links
def irs_form(form_name, min_year, max_year):

    modi_form_name = form_name.replace(' ', '+')

    url = f'https://apps.irs.gov/app/picklist/list/priorFormPublication.html?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow=0&criteria=formNumber&value={modi_form_name}&isDescending=false'

# Handle input error
    try:
        df = pd.read_html(url)[3]
    except:
        df = []
        links_list = []
        print(f'There is not exact match to {form_name}, please try again!')
        
        return links_list
    # df = pd.read_html(url)[3]

#   Filter IRS web content and extract the targeted table
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find_all('table')[3]


#   Pull out links from table and append to a list
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
     
    links_list = df['Link'].tolist()
    return links_list



irs_links_list = irs_form(form_name, min_year, max_year)

# Create subdirectory and save downloaded files
for link in irs_links_list:
    r = requests.get(link)
    if not os.path.exists(f'{form_name}'):
        os.makedirs(f'{form_name}')
    os.chdir(f'{form_name}')  
    file_year = link[len(link)-8:len(link)-4]
    save_name = f'{form_name}-{file_year}.pdf'
    open(save_name, 'wb').write(r.content)
    os.chdir('..')
