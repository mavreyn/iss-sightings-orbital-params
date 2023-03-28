
'''
Basic script I made to start my web scraping journey
Using Heaven's Above to retrive ISS orbital parameters
Pretty much my first 'real' script I've ever wrote tbh

Maverick Reynolds
01-15-2022

'''

import requests
from bs4 import BeautifulSoup
import re
import csv


UCF_PARAMS = {
    'satid': 25544,
    'lat': 28.6144,
    'lng': -81.1965,
    'alt': 0,
    'tz': 'EST'
}

PASSES_HEADER = [
    'Date',
    'Brightness (mag)',
    'Start Time',
    'Start Alt.',
    'Start Az.',
    'Highest Point Time',
    'Highest Point Alt.',
    'Highest Point Az.',
    'End Time',
    'End Point Alt.',
    'End Point Az.',
    'Pass type',
]

# Scrape parameters from Heavens Above
def get_iss_orbital_parameters(loc_params) -> dict:
    # Make request
    url = 'https://www.heavens-above.com/orbit.aspx'
    resp = requests.get(url, params=loc_params)

    # Parse text and find parameter lines
    soup = BeautifulSoup(resp.text, 'html.parser')
    txt = soup.get_text()
    matches = re.findall('^([\w\(\)\ ]+)\:\ (.+)$', txt, flags=re.M)

    # Make dict with regex groups from matches
    orbital_parameters = dict()
    for match in matches:
        orbital_parameters[match[0]] = match[1]
    
    return orbital_parameters

# Write header and data to a csv
def write_csv_and_header(head, data):
    with open('PASSES.csv', 'w', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(head)
        writer.writerows(data)


# Puts data from a table into a list
def get_table_data(table):

    def get_table_row_data(table_row):    
            return [element.get_text(strip=True) for element in table_row.find_all('td')]

    table_rows = table.find_all('tr', {'class': 'clickableRow'})

    return [get_table_row_data(row) for row in table_rows]


# Scrape sighting data from Heavens Above
def write_iss_sightings(loc_params):
    # Make request
    url = 'https://www.heavens-above.com/PassSummary.aspx'
    resp = requests.get(url, params=loc_params)

    # Parse text, find table info
    soup = BeautifulSoup(resp.text, 'html.parser')
    table = soup.find('table', {'class': 'standardTable'})
    table_data = get_table_data(table)

    # Write the data to a csv
    write_csv_and_header(PASSES_HEADER, table_data)


def main():
    orbital_params = get_iss_orbital_parameters(UCF_PARAMS)
    for key, value in orbital_params.items():
        print(key, ':', value)
    
    print()
    write_iss_sightings(UCF_PARAMS)
    with open('PASSES.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)

    input() 

if __name__ == '__main__':
    main()

