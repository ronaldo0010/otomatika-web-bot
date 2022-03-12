from urllib import request
from bs4 import BeautifulSoup 
import pandas as pd
import requests, csv, sqlite3
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def get_table(url, target_id):
    '''
        returns a panda data frame 
    '''

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

    # Create the dataframe from table data
    return pd.DataFrame(rows, columns=headers)


def setup_connection():
    return sqlite3.connect('test2.db')


def create_col_query(headers):
    temp = "("
    for col in headers:
        temp += (col.strip("/") + ',')
    temp += ")"
    
    return temp


def save_to_db(df, headers, table):
    # setup connection
    conn = setup_connection()
    df.to_sql(table, conn, if_exists="append", index=False)
    conn.commit()

    print("success")
    
def create_csv(df):
    df.to_csv("Countries.csv", index=False, sep=',')
    
    
def get_top_10(df):
    return df[2:12]
    
    
def take_screenshot(url, state, driver, browser, ID):
    name = get_name(state)
    driver.get(url)
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, ID))
    )
    element = driver.find_element(By.ID, ID)
    element.screenshot(name)
    
    return name
    
def get_name(name):
    fname = "{}.png".format(name)
    i = 1
    for i in range(0,3):
        if not os.path.isfile(fname):
            break
            
        i += 1
    return fname
    
def save_report(files):
    ''' does the ppt thing'''
    counter = 1
    for file in files:
        if counter % 4 == 0:
            break
            # create new file
        else:
            # append to current file
            break
        counter += 1
    
def process_report(tbl, url):
    browser = ChromeDriverManager().install()
    driver = webdriver.Chrome(browser)
    
    file_names = []
    ls = ["coronavirus-deaths-linear", "coronavirus-cases-linear", "graph-cases-daily", "graph-active-cases-total"]
    k = 0
    for i in get_top_10(tbl).USAState:
       
        state = i.strip('\n').strip()
        state_url = "{}/{}".format(url, state).replace(" ", '-')
        for ID in ls: 
            name = take_screenshot(state_url, state, driver, browser, ID)
            file_names.append(name)

    driver.close()
        
    return file_names


url = "https://www.worldometers.info/coronavirus/"
target_id = "main_table_countries_today"

tbl = get_table(url, target_id)
create_csv(tbl)

tbl = tbl.drop(columns='#')

headers = tbl.columns
table_name = "COUNTRIES"
save_to_db(tbl, headers, table_name)

country = "US"
url = "{}/country/{}".format(url, country)
target_id = "usa_table_countries_today"

tbl = get_table(url, target_id)
create_csv(tbl)
headers = tbl.columns
table_name = "american_states"

save_to_db(tbl, headers, table_name)

url = "https://www.worldometers.info/coronavirus/usa"
files = process_report(tbl, url)


save_reports(files)