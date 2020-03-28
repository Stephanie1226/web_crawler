"""
1. Change your file path in line 25 and line 83 !!!
2. Download webdriver from here: https://sites.google.com/a/chromium.org/chromedriver/downloads
3. Change your webdriver path in line 50 !!!
"""

import os
import sys
import time
import re
import csv
import random
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
#from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


class open_csv():
    def __init__(self):
        #CHANGE YOUR PATH HERE
        self.path = '/Users/Stephanie/Desktop/classical_yt_file.csv'

    def open_read(self):
        data = pd.read_csv(self.path, index_col=0)
        return data

class youtube_search():
    def __init__(self):
        self.url = "https://www.youtube.com/"
        self.keywords = ""
        self.yt_urls = []

    def search(self, data):
        youtube_home = self.url

        #For fake user-sgent
        """
        options = Options()
        ua = UserAgent()
        userAgent = ua.random
        options.add_argument(f'user-agent={userAgent}')
        driver = webdriver.Chrome(chrome_options=options, executable_path="/Users/Stephanie/webapp/chromedriver") # Use Chrome
        """

        #CHANGE YOUR webdriver PATH HERE !!!
        driver = webdriver.Chrome(executable_path="/Users/Stephanie/webapp/chromedriver")
        driver.get(youtube_home)
        col_num = data.shape[1]

        for i in range (data.shape[0]):
            search_space = driver.find_element_by_name('search_query')
            search_space.clear()

            self.keywords = data.iloc[i,col_num-1]
            search_space.send_keys(self.keywords)
            search_space.send_keys(Keys.RETURN)
            key_page = driver.current_url
            driver.get(key_page)
            #time.sleep(random.randint(4,9))

            try:
                if driver.find_element_by_xpath('(//*[@id="video-title"])[1]').is_displayed():
                    first_link = driver.find_element_by_xpath('(//*[@id="video-title"])[1]')
                    video_url = first_link.get_attribute('href')
                    video_url = video_url.lstrip("https://www.youtube.com/watch?v=")
                    self.yt_urls.append(video_url)
            except:
                video_url = ""
                self.yt_urls.append(video_url)
            
        return self.yt_urls

class save_new_csv():
    def __init__(self):
        self.path = ""
    
    def save(self, data, urls):
        #CHANGE PATH HERE
        self.path = '/Users/Stephanie/Desktop/classical_yt_file.csv'
        data.loc[:, 'youtube_link'] = urls
        data.to_csv(self.path, index=True, header=True)
        #data.to_csv(self.path, header=True)


if __name__=='__main__':
    url = []
    
    OpenCsv = open_csv()
    data = OpenCsv.open_read()

    YoutubeSearch = youtube_search()
    urls = YoutubeSearch.search(data)

    SaveCsv = save_new_csv()
    SaveCsv.save(data, urls)







