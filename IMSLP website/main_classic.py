"""
1. Change your file path in line 141 and line 149 !!!
"""

import urllib.request as req
from urllib.parse import quote
import string
import bs4
import re
import time
import random
import csv

class getWorkTypesURLs():
    def __init__(self):
        self.workTypesTitles = []
        self.workTypesURLs = []
        
    def get_worktype_urls(self):
        url = "https://imslp.org/wiki/IMSLP:View_Genres/Work_Types"
        request=req.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
        })
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")

        root = bs4.BeautifulSoup(data, "html.parser")
        finding = root.find_all("span", class_ = "plainlinks")

        for info in finding:
            if info.a != None:
                url = info.a.get('href')
                self.workTypesTitles.append(info.a.string)
                self.workTypesURLs.append(url)

        return self.workTypesTitles, self.workTypesURLs

class getCompositionURLs():
    def __init__(self):
        self.pre_link = "https://imslp.org"
        self.composition_links = []

    def get_composition_urls(self, urlIn):
        url = urlIn
        request=req.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        })
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")

        root = bs4.BeautifulSoup(data, "html.parser")
        finding = root.find_all("a", {'class':'categorypagelink'})

        for info in finding:
            if info != None:
                link = info.get('href')
                url = self.pre_link + link
                self.composition_links.append(url)

        return self.composition_links

class getNext200():
    def __init__(self):
        self.pre_link = "https://imslp.org"
        self.next_link = ""

    def get_next200_url(self, urlIn):
        url = urlIn
        request=req.Request(url, headers={
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        })
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")

        root = bs4.BeautifulSoup(data, "html.parser")
        find_next200 = root.find("a", text = re.compile("next 200"))
        if find_next200 != None: 
            link = find_next200.get('href')
            self.next_link = self.pre_link + link
        else:
            self.next_link = None

        return self.next_link

class getCompositionInfo():
    def __init__(self):
        self.music_name = ""
        self.composer_name = ""
        self.composer_genre = ""
        self.composition_genre = ""
        self.date = ""

    def get_info(self, urlIn):
        url = urlIn
        url = quote(url, safe = string.printable) #to solve the encoding problem
        request=req.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        })
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")

        root = bs4.BeautifulSoup(data, "html.parser")

        music_name_tag = root.find("h1", {'class':'firstHeading pagetitle page-header'})
        if music_name_tag != None:
            music_name = music_name_tag.string
            self.music_name = music_name.lstrip()
        else:
            self.music_name = None

        name_title = root.find("th", text = re.compile("Composer"))
        if name_title != None:
            name_tag = name_title.find_next_sibling("td")
            self.composer_name = name_tag.a.string
        else:
            self.composer_name = None

        genre_title = root.find("th", text = re.compile("Piece Style"))
        if genre_title != None:
            genre_tag = genre_title.find_next_sibling("td")
            self.composition_genre = genre_tag.a.string
        else:
            self.composition_genre = None

        date_title = root.find("span", text = re.compile("Date of Composition"))
        if date_title != None:
            parent_tag = date_title.parent
            date_tag = parent_tag.find_next_sibling("td")
            self.date = date_tag.string
        else:
            self.date = None

        return self.composer_name, self.composition_genre, self.date, self.music_name

class save_to_csv():
    def __init__(self):
        self.path = ""
    
    def creat_csv(self):
        #CHANGE YOUR PATH HERE
        self.path = "/classical_imslp_file.csv"
        with open(self.path, 'w') as file_:
            csv_write = csv.writer(file_)
            csv_head = ["composer", "genre","work_type","year","composition_name"]
            csv_write.writerow(csv_head)

    def write_csv(self, Composer, Genre, Work_type, Year, Coposition_name):
        #CHANGE YOUR PATH HERE
        self.path = "/classical_imslp_file.csv"
        with open(self.path, 'a') as file_:
            csv_write = csv.writer(file_)
            data_row = [Composer, Genre, Work_type, Year, Coposition_name]
            csv_write.writerow(data_row)


if __name__=='__main__':
    start_time = time.time()
    work_type_titles = []
    work_type_urls = []
    composition_links = []
    work_type = ""
    composer = ""
    composer_genre = ""
    genre = ""
    date = ""
    composition_name = ""

    WorkTypeURLs = getWorkTypesURLs()
    work_type_titles, work_type_urls = WorkTypeURLs.get_worktype_urls()

    switch = 1
    #for work_type_url in work_type_urls:
    for count in range(2, 3):
        print(work_type_titles[count])
        CompositionURL = getCompositionURLs()
        wt_currentURL = work_type_urls[count]
        composition_links = CompositionURL.get_composition_urls(wt_currentURL)
        work_type = work_type_titles[work_type_urls.index(wt_currentURL)] 
        time.sleep(random.randint(1, 5))

        while True:
            for link in composition_links:
                Information = getCompositionInfo()
                composer, genre, date, composition_name = Information.get_info(link)

                save_to_file = save_to_csv()
                if switch == 1:
                    save_to_file.creat_csv()
                    save_to_file.write_csv(composer, genre, work_type, date, composition_name)
                else:
                    save_to_file.write_csv(composer, genre, work_type, date, composition_name)
                switch = 0
                time.sleep(random.randint(1, 5))
            
            # Next Page
            Next200url = getNext200()
            next_200_url = Next200url.get_next200_url(wt_currentURL)
            if next_200_url != None:
                wt_currentURL = next_200_url
                CompositionURL = getCompositionURLs()
                composition_links = CompositionURL.get_composition_urls(wt_currentURL) 
            else:
                break

    #print("----- %s seconds------" % (time.time()-start_time))
