import requests
from bs4 import BeautifulSoup

import json
from time import sleep

URL = 'http://www2.dallascityhall.com/FoodInspection/SearchScoresAction.cfm'

formData = {
    'NAME': '',
    'STNO': '',
    'STNAME': '',
    'ZIP': '75396',
    'Submit': 'Search+Scores'
}

zipStart = 75201
zipStop = 75398

per_page_delay = 3

dat_file = 'data.json'

jsonList = []
totalInspections = 0

# iterate over Dallas ZIP codes
for zip in range(zipStart, zipStop + 1):
    print(zip)
    formData['ZIP'] = zip
    params = {}
    page = 1
    lastPage = 1
    hashyData = {}
    # iterate over pages
    while page == 1 or page <= lastPage:
        if page > 1:
            params = {'PageNum_q_search': page}
        response = requests.post(URL, params=params, data=formData)
        soup = BeautifulSoup(response.content, 'html.parser')
        tables = soup.findAll('table')
        if len(tables) < 3:
            # bail out, no search results
            print('  no records')
            sleep(per_page_delay)
            break
        mainTable = tables[1]
        pageInspections = 0
        for row in mainTable.findAll('tr')[1:]:
            # td 0:Name 1:Address 2:Suite 3:Zip 4:Mapsco 5:Inspected 6:Score 7:Inspection Type
            td = row.findAll('td')
            name = td[0].text
            address = ' '.join(td[1].find('a').text.split())
            suite = td[2].text
            NAS = name + address + suite

            if not NAS in hashyData:
                hashyData[NAS] = {
                    'name': name,
                    'address': address,
                    'suite': suite,
                    'zip': zip,
                    'inspections': []
                }
            
            hashyData[NAS]['inspections'].append({
                'inspected': td[5].text,
                'score': int(td[6].text)
            })
            pageInspections += 1
            totalInspections += 1

        for a in soup.findAll('a'):
            if a.text == 'Last':
                hrefSplit = a['href'].split('=')
                if len(hrefSplit) == 2 and hrefSplit[0].startswith('SearchScoresAction.cfm'):
                    lastPage = int(hrefSplit[1])
        
        print('  page {0:>2} of {1:>2} -> {2:>3} records'.format(page, lastPage, pageInspections))
        sleep(per_page_delay)
        page += 1

    # add all the hashed locations to the json list without the hash
    for NAS, locationData in hashyData.items():
        jsonList.append(locationData)

with open(dat_file, 'w') as dat:
    dat.write(json.dumps(jsonList, sort_keys=True, indent=4))

print('Scraped', totalInspections, 'inspection records for', len(jsonList), 'locations')
print('Done.')
