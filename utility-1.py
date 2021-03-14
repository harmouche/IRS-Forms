import pandas as pd
import json
import requests
from bs4 import BeautifulSoup

irs_list = ['Form W-2', 'Form 1095-C', 'Form 1099-MISC', 'Form W-2P']


# Takes a form name and returns a JSON format as requierd
def irs_form(form_name):

    modi_form_name = form_name.replace(' ', '+')

    url = f'https://apps.irs.gov/app/picklist/list/priorFormPublication.html?resultsPerPage=200&sortColumn=sortOrder&indexOfFirstRow=0&criteria=formNumber&value={modi_form_name}&isDescending=false'

# Handle input error
    try:
        df = pd.read_html(url)[3]
    except:
        print("print table none")
        df = []
        print("df empty", df)
        new_result = {}
        output = json.dumps(new_result)
        return output
    
#   Filter IRS web content and extract the targeted table
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find_all('table')[3]

#   Pull out links from table and append to dataframe
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


    if len(df[df['Product Number'] == form_name]) == 0:
        df = []
        print(f'There is not exact match to {form_name}, please try again!')
    else:
        df = df[df['Product Number'] == form_name]

#   Format output as required
        new_result = {
        "form_number": df.iloc[1,0],
        "form_title": df.iloc[1,1],
        "min_year": int(df['Revision Date'][df['Revision Date'].idxmin()]),
        "max_year": int(df['Revision Date'][df['Revision Date'].idxmax()])}

        output = json.dumps(new_result)
        return output


# Take a list (IRS form names), returns a list of required JSON output
def irs_forms(irs_list):
    output_list = []
    for element in irs_list:
        if irs_form(element) == {}:
            pass
        else:
            output_list.append(irs_form(element))
    return output_list
    
# Print for verification
print(irs_forms(irs_list))