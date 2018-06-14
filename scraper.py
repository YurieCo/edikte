import scraperwiki

# Blank Python

import scraperwiki
import lxml.html

URL = "http://www.edikte.justiz.gv.at/edikte/ex/exedi3.nsf/suche?OpenForm&subf=v&query=%5BBL%5D%3D5"

web_page = lxml.html.parse(URL)

table_of_insolvencies = web_page.find('//table/tbody')

for row in table_of_insolvencies.findall('tr'):
    cells = row.findall('td')
    nr, type, adresse , objektbezeichnung,  = cells
    
    data = {}

    details_link = type.find('a')
    data['reference'] = details_link.text
    data['link'] = details_link.get('href')
    data['adresse _name'] = adresse.text

    remaining_lines = [d.tail for d in adresse .findall('br')]
    if len(remaining_lines) == 2:
        data['adresse _postcode'] = remaining_lines[0]
        data['adresse _town'] = remaining_lines[1]
    else:
        data['adresse _town'] = remaining_lines[0] 

    data['adresse _postcode'], data['adresse _town'] = data['adresse _town'].split(" ", 1)
    
    scraperwiki.sqlite.save(unique_keys=['reference'], data=data)
