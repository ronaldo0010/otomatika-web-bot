from urllib import request
from bs4 import BeautifulSoup 
import pandas as pd
import requests


def get_table(url):
    '''
        returns a panda data frame 
    '''
    target_id = "main_table_countries_today"

    markup = requests.get(url)
    soup =  BeautifulSoup(markup.content, "html.parser")

    soup = soup.find(id=target_id)

    headers = []
    for h in soup.findAll('th'):
        headers.append(h.text)

    rows = []
    for row in soup.findAll('tr'):
        row_data = []
        for cell in row.findAll('td'):
            row_data.append(cell.text)
        rows.append(row_data)

    # Create the dataframe from your table data
    return pd.DataFrame(rows[9:], columns=headers)

def setup_connection(connection_string):
    return None

def save_to_db(file, connection_string):
    # setup connection
    db = setup_connection(connection_string)
    # write to db 
    

url = "https://www.worldometers.info/coronavirus/"
tbl = get_table(url)

print(tbl)

