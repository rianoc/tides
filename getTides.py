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
rotated = [list(col) for col in zip(*output_rows)]
index = sorted(range(len(rotated[0])), key=lambda k: rotated[0][k])
times = [rotated[1][i] for i in index]
heights = [rotated[2][i] for i in index]
heights = list(map(lambda x: x[:-1],heights))
labels = ['H1T','H2T','L1T','L2T','H1H','H2H','L1H','L2H']
info = times + heights
out = []
for i in range(len(info)):
    out.append(labels[i]+","+info[i])
with open(LOCATION+'/tides.csv', "w") as output:
    for l in out:
        output.write(str(l+'\n'))