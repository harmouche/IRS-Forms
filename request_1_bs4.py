import requests
from bs4  import BeautifulSoup
import pandas as pd


formName = input("Enter form name here: ").replace(' ', '+')


url = f'https://apps.irs.gov/app/picklist/list/priorFormPublication.html?value={formName}&criteria=formNumber&submitSearch=Find'

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

irs_forms_table = soup.find('table', class_ = 'picklist-dataTable')

# print(irs_forms_table)
# df = pd.read_html(url)

# print(df)

for form in irs_forms_table.find_all('tr'):
    form_list_number = form.find_all('td', class_ = 'LeftCellSpacer')
    form_list_name = form.find_all('td', class_ = 'MiddleCellSpacer')
    form_list_year = form.find_all('td', class_ = 'EndCellSpacer')
    for file in form_list_number:
        file_link = file.find_all('a')
    print(form_list_number, form_list_name, form_list_year, file_link)
