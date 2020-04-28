import requests
from bs4 import BeautifulSoup
from config import URL
from config import LOCATION

html = requests.get(URL).text
data = BeautifulSoup(html, 'html.parser')

tab = (data.findAll("table", {"class": "vis3"}))[0]

output_rows = []
for table_row in tab.findAll('tr'):
    columns = table_row.findAll('td')
    output_row = []
    for column in columns:
        output_row.append(column.text)
    output_rows.append(output_row)

del output_rows[0:2]
out = []
for i in range(len(output_rows)):
    out.append(",".join(output_rows[i]))
with open(LOCATION+'/tides.csv', "w") as output:
    for l in out:
        output.write(str(l+'\n'))

