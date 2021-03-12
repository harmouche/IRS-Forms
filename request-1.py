import requests
from bs4 import BeautifulSoup
import json

formName = input("Enter form name here: ")

payload = {
    "value": formName,
    "criteria": "formNumber",
    "submitSearch": "Find" }

result = requests.get("https://apps.irs.gov/app/picklist/list/priorFormPublication.html", payload)

src = result.content

soup = BeautifulSoup(src, 'html.parser')

formsList = soup.find_all("tr")

for form in formsList:
    if formName in form.text:
        if formName == form.a.contents[0]:
            print(form)

