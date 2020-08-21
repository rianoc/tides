import requests
from bs4 import BeautifulSoup
from config import URL
from config import LOCATION

xml = requests.get(URL).text
data = BeautifulSoup(xml, 'xml')

description = (data.findAll("description"))[1].getText()
tides = BeautifulSoup(description, 'html.parser')
tides = (str(tides).split('<br/>'))[2:-1]

output_rows = []
for table_row in tides:
    s = table_row.split(' - ')
    s1 = s[1].split(' (')
    output_rows.append([s1[0],s[0],s1[1][:-1]])

out = []
for i in range(len(output_rows)):
    out.append(",".join(output_rows[i]))
with open(LOCATION+'/tides.csv', "w") as output:
    for l in out:
        output.write(str(l+'\n'))
