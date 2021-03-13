import requests
from bs4 import BeautifulSoup
import json

formName = input("Enter form name here: ")

payload = {
    "value": formName,
    "criteria": "formNumber",
    "submitSearch": "Find" }

result = requests.get("https://apps.irs.gov/app/picklist/list/priorFormPublication.html", payload)

src = result.text
# print("Results in JSON format: ", result.json())

soup = BeautifulSoup(src, 'html.parser')

formsList = soup.find_all("tr")

for form in formsList:
    if formName in form.text:
        if formName == form.a.text:
            for td in formsList.find_all("td"):
                print(td)
            # print(form.a.href)
            # filteredData = json.dumps({
            #     "form_number": form.a.contents[0],
            #     "form_title": form.td.contents[0],
            #     "year": form.td.contents[1],                
            # })
            # print(filteredData)


