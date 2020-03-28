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
        if music_name_tag is not None and music_name_tag.string is not None:
            music_name = music_name_tag.string
            self.music_name = music_name.lstrip()
        else:
            self.music_name = None

        name_title = root.find("th", text = re.compile("Composer"))
        if name_title != None:
            name_tag = name_title.find_next_sibling("td")
            if name_tag is not None and name_tag.a is not None:
                self.composer_name = name_tag.a.string
            else:
                self.composer_name = None

        else:
            self.composer_name = None

        genre_title = root.find("th", text = re.compile("Piece Style"))
        if genre_title != None:
            genre_tag = genre_title.find_next_sibling("td")
            if genre_tag is not None and genre_tag.a is not None:
                self.composition_genre = genre_tag.a.string
            else:
                self.composition_genre = None
        else:
            self.composition_genre = None

        date_title = root.find("span", text = re.compile("Date of Composition"))
        if date_title != None:
            parent_tag = date_title.parent
            date_tag = parent_tag.find_next_sibling("td")
            if date_tag is not None and date_tag.string is not None:
                self.date = date_tag.string
            else:
                self.date = None
        else:
            self.date = None

        return self.composer_name, self.composition_genre, self.date, self.music_name

class get_trans_alias():
    def __init__(self):
        self.translations = []
        self.aliases = []

    def get_tnaInfo(self, urlIn):
        url = urlIn
        url = quote(url, safe = string.printable)
        request=req.Request(url, headers={
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        })
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")

        root = bs4.BeautifulSoup(data, "html.parser")

        find_transtag = root.find("th", text = re.compile("Name Translations"))
        if find_transtag != None:
            trans_parenttag = find_transtag.find_next_sibling("td")
            translations = trans_parenttag.find_all("span")

            for trans in translations:
                if trans.string != None:
                    self.translations.append(trans.string)
                else:
                    pass
        else:
            self.translations = None

        find_aliastag = root.find("th", text = re.compile("Name Aliases"))
        if find_aliastag != None:
            aliases_parenttag = find_aliastag.find_next_sibling("td")
            aliases = aliases_parenttag.find_all("span")

            for alias in aliases:
                if alias.string != None:
                    self.aliases.append(alias.string)
                else:
                    pass
        else:
            self.aliases = None

        return self.translations, self.aliases

class save_to_csv1():
    def __init__(self):
        self.path = "/Users/Stephanie/Desktop/classical_test1_file.csv"
    
    def creat_csv(self):
        with open(self.path, 'w') as file_:
            csv_write = csv.writer(file_)
            csv_head = ["composer", "genre","work","year","composition"]
            csv_write.writerow(csv_head)

    def write_csv(self, Composer, Genre, Work_type, Year, Coposition_name):
        with open(self.path, 'a') as file_:
            csv_write = csv.writer(file_)
            data_row = [Composer, Genre, Work_type, Year, Coposition_name]
            csv_write.writerow(data_row)

class save_to_csv2():
    def __init__(self):
        self.path = "/Users/Stephanie/Desktop/classical_test2_file.csv"

    def creat_csv(self):
        with open(self.path, 'w') as file_:
            csv_write = csv.writer(file_)
            csv_head = ["composition", "as_known_as"]
            csv_write.writerow(csv_head)

    def write_csv(self, composition_name, translations, aliases):
        with open(self.path, 'a') as file_:
            csv_write = csv.writer(file_)
            if translations != None:
                for trans in translations:
                    data_row = [composition_name, trans]
                    csv_write.writerow(data_row)
            else:
                pass

            if aliases != None:
                for alias in aliases:
                    data_row = [composition_name, alias]
                    csv_write.writerow(data_row)
            else:
                pass


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
    translations = []
    aliases = []

    WorkTypeURLs = getWorkTypesURLs()
    work_type_titles, work_type_urls = WorkTypeURLs.get_worktype_urls()

    switch1 = switch2 = 1
    #for count in range(2): #for testing
    for count in range(212, 265):
        print(work_type_titles[count])
        CompositionURL = getCompositionURLs()
        wt_currentURL = work_type_urls[count]
        composition_links = CompositionURL.get_composition_urls(wt_currentURL)
        work_type = work_type_titles[work_type_urls.index(wt_currentURL)] #測試
        time.sleep(random.randint(0,2))

        while True:
            for link in composition_links:
                Information = getCompositionInfo()
                composer, genre, date, composition_name = Information.get_info(link)

                Trans_Aliases = get_trans_alias()
                translations, aliases = Trans_Aliases.get_tnaInfo(link)

                # Save composer, genre, date and composition information
                save_to_file1 = save_to_csv1()
                if switch1 == 1:
                    save_to_file1.creat_csv()
                    save_to_file1.write_csv(composer, genre, work_type, date, composition_name)
                    switch1 = 0
                else:
                    save_to_file1.write_csv(composer, genre, work_type, date, composition_name)

                # Save translations and aliases (if exit)
                if (translations == None) and (aliases == None):
                    pass
                else:
                    save_to_file2 = save_to_csv2()
                    if switch2 == 1:
                        save_to_file2.creat_csv()
                        save_to_file2.write_csv(composition_name, translations, aliases)
                        switch2 = 0
                    else:
                        save_to_file2.write_csv(composition_name, translations, aliases)

                time.sleep(random.randint(0,2))
            
            # Next Page
            Next200url = getNext200()
            next_200_url = Next200url.get_next200_url(wt_currentURL)
            if next_200_url != None:
                wt_currentURL = next_200_url
                CompositionURL = getCompositionURLs()
                composition_links = CompositionURL.get_composition_urls(wt_currentURL) 
            else:
                break

    print("----- %s seconds------" % (time.time()-start_time))

"""
    for work_type_url in work_type_urls:
        CompositionURL = getCompositionURLs()
        composition_links = CompositionURL.get_composition_urls(work_type_url)
        work_type = work_type_titles[work_type_urls.index(work_type_url)]
"""