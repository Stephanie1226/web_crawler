"""
1. Change your file path in line 22 and line 77 !!!
2. Download webdriver from here: https://sites.google.com/a/chromium.org/chromedriver/downloads
3. Change your webdriver path in line 43 !!!
"""

import sys
import time
import re
import csv
import random
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

class open_csv():
    def __init__(self):
        #CHANGE YOUR PATH HERE
        self.path = '/Users/Stephanie/Desktop/pop_google_file.csv'

    def open_read(self):
        data = pd.read_csv(self.path, index_col=0)
        return data

class google_search():
    def __init__(self):
        self.url = "https://www.google.com/"
        self.keywords = ""
        self.genre = []

    def search(self, data):
        google_home = self.url

        options = Options()
        ua = UserAgent()
        userAgent = ua.random
        options.add_argument(f'user-agent={userAgent}')

        #CHANGE YOUR webdriver PATH HERE !!!
        driver = webdriver.Chrome(chrome_options=options, executable_path="/Users/Stephanie/webapp/chromedriver") # Use Chrome
        driver.get(google_home)
        col_num = data.shape[1]

        #for i in range (19): #for testing
        for i in range (data.shape[0]): 
            search_space = driver.find_element_by_name('q')
            search_space.clear()
            self.keywords = data.iloc[i,1] + " " + data.iloc[i,col_num-2]
            search_space.send_keys(self.keywords)
            search_space.send_keys(Keys.RETURN)
            
            key_page = driver.current_url
            driver.get(key_page)

            root = BeautifulSoup(driver.page_source, "html.parser")
            finding = root.find("div", attrs = {'data-attrid':'kc:/music/recording_cluster:skos_genre'})

            if finding != None:
                find_genre = finding.find("span", class_ = "LrzXr kno-fv")
                self.genre.append(find_genre.string)
            else:
                #self.genre.append("No genre")
                self.genre.append("")

        driver.quit()
        return self.genre

class save_new_csv():
    def __init__(self):
        self.path = ""
    
    def save(self, data, genres):
        #CHANGE YOUR PATH HERE
        self.path = '/Users/Stephanie/Desktop/pop_google_file.csv'
        data.loc[:, 'genre'] = genres
        data.to_csv(self.path, index=False, header=True)
        

if __name__=='__main__':
    url = []
    
    OpenCsv = open_csv()
    data = OpenCsv.open_read()

    GoogleSearch = google_search()
    genres = GoogleSearch.search(data)
    #print(genres)

    SaveCsv = save_new_csv()
    SaveCsv.save(data, genres)






