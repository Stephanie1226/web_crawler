"""
Change your file path in line 317 and line 330 !!!
"""
# Change random time
# Change User-Agent

import urllib.request as req
import pandas as pd
from collections import Counter
import dataloader as dtl
import bs4
import re
import time
import random
import csv


class get_page_artists():
    def __init__(self):
        self.page_artists = []

    def getArtistsNames(self, urlIn):
        url = urlIn
        request=req.Request(url, headers={
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        })
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")
        root = bs4.BeautifulSoup(data, "html.parser")

        finding = root.find("table", class_ = "tbl")
        artists_links = finding.find_all("a", href = re.compile('artist'))
        for link in artists_links:
            if link.bdi != None:
                artist_link = link.get('href')
                self.page_artists.append(artist_link)
        return self.page_artists

class check_area():
    def __init__(self):
        self.area = ""
    
    def get_area(self, urlIn):
        url = urlIn
        request=req.Request(url, headers={
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        })
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")
        root = bs4.BeautifulSoup(data, "html.parser")
        find_area = root.find("dd", class_ = "area")
        if find_area is not None and find_area.bdi is not None:
            self.area = find_area.bdi.string
        else:
            pass
        return self.area

class get_all_albums_info():
    def __init__(self):
        self.suburl = "https://musicbrainz.org"
        self.artistName = ""
        self.category = ""
        self.albums = []
        self.albums_urls = []

    def getAlbums(self, urlIn):
        url = urlIn
        request=req.Request(url, headers={
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        })
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")

        root = bs4.BeautifulSoup(data, "html.parser")

        artist_name = root.find("div", class_ = re.compile('artistheader'))
        self.artistName = artist_name.h1.a.bdi.string
        artist_categ = root.find("p", class_ = "subheader")
        categ_ = artist_categ.text

        if categ_ == "~ Person":
            self.category = "1"
        elif categ_ == "~ Group":
            self.category = "2"
        else:
            self.category = "3"

        finding = root.find_all("a", href = re.compile('release-group'))
        for links in finding:
            link = links.get('href')
            url = self.suburl + link
            self.albums_urls.append(url)
        
        for album_names in finding:
            if album_names is not None and album_names.bdi is not None:
                self.albums.append(album_names.bdi.string)

        return self.artistName, self.albums, self.albums_urls, self.category

class get_same_albums_URLs():
    def __init__(self):
        self.sameAlbumLinks = []
        self.suburl = "https://musicbrainz.org"

    def getURLs(self, urlIn, artist):
        url = urlIn
        request=req.Request(url, headers={
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        })
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")

        root = bs4.BeautifulSoup(data, "html.parser")
        # finding = root.find(text = re.compile("Release group by"))
        finding = root.find("p", class_ = "subheader")
        first_artist_tag = finding.find("a", href = re.compile("artist"))

        first_artist = first_artist_tag.bdi.string
        if first_artist == artist:
            find_oddrows = root.find_all("tr", class_ = "odd")
            for odd in find_oddrows:
                odd_tag = odd.find("a", href = re.compile('release'))
                odd_link = odd_tag.get('href')
                odd_link = self.suburl + odd_link
                self.sameAlbumLinks.append(odd_link)
            find_evenrows = root.find_all("tr", class_ = "even")
            for even in find_evenrows:
                even_tag = even.find("a", href = re.compile('release'))
                even_link = even_tag.get('href')
                even_link = self.suburl + even_link
                self.sameAlbumLinks.append(even_link)
        else:
            pass
        return self.sameAlbumLinks

class get_Song():
    def __init__(self):
        self.date = ''
        self.songs = []
        self.feat_urls = []

    def get_Songs(self, input_url, artist_name):
        url = input_url
        request=req.Request(url, headers={
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        })
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")

        root = bs4.BeautifulSoup(data, "html.parser")

        date = root.find("span", class_ = "release-date")
        if date != None:
            self.date = date.string

        # Name if the songs
        find_odds = root.find_all("tr", class_ = "odd")
        for odd in find_odds:
            odd_song = odd.find("a", href = re.compile('recording'))
            if odd_song.bdi != None:
                self.songs.append(odd_song.bdi.string)
        find_evens = root.find_all("tr", class_ = "even")
        for even in find_evens:
            even_song = even.find("a", href = re.compile('recording'))
            if even_song.bdi != None:
                self.songs.append(even_song.bdi.string)

        # Find related artists
        find_oddrelated = root.find_all("tr", class_ = "odd")
        for odd_relate in find_oddrelated:
            relate_feat = odd_relate.find(text = re.compile("feat"))
            relate_collab = odd_relate.find(text = re.compile("&"))

            if relate_feat != None:
                parent_tag = relate_feat.parent
                all_related = parent_tag.find_all("a", href = re.compile("artist"))
                for artist in all_related:
                    artist_url = artist.get('href')
                    self.feat_urls.append(artist_url)

            elif relate_collab != None:
                parent_tag = relate_collab.parent
                all_related = parent_tag.find_all("a", href = re.compile("artist"))
                for artist in all_related:
                    artist_url = artist.get('href')
                    self.feat_urls.append(artist_url)
            else:
                pass

        find_evenrelated = root.find_all("tr", class_ = "even")
        for even_relate in find_evenrelated:
            relate_feat = even_relate.find(text = re.compile("feat"))
            relate_collab = even_relate.find(text = re.compile("&"))

            if relate_feat != None:
                parent_tag = relate_feat.parent
                all_related = parent_tag.find_all("a", href = re.compile("artist"))
                for artist in all_related:
                    artist_url = artist.get('href')
                    self.feat_urls.append(artist_url) 
            elif relate_collab != None:
                parent_tag = relate_collab.parent
                all_related = parent_tag.find_all("a", href = re.compile("artist"))
                for artist in all_related:
                    artist_url = artist.get('href')
                    self.feat_urls.append(artist_url)
            else:
                pass
        return self.date, self.songs, self.feat_urls

class get_features():
    def __init__(self):
        self.suburl = "https://musicbrainz.org"
        self.name = ""
    
    def getNames(self, artist_url, artist, features, category):
        # Check if the artist is a person or group
        url = artist_url + "/relationships"
        request = req.Request(url, headers={
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        })
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")
        root = bs4.BeautifulSoup(data, "html.parser")

        if category == "1": # It's a person
            finding = root.find("th", text = re.compile('member of'))
            if finding != None:
                parent_tag = finding.parent
                find_group = parent_tag.find_all("a", href = re.compile('artist'))
                for group in find_group:
                    group_url = group.get('href')
                    group_weights = [group_url]*300
                    features.extend(group_weights)
                    # then, get group members in every group
                    url = self.suburl + group_url + "/relationships"
                    request = req.Request(url, headers={
                        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
                    })
                    with req.urlopen(request) as response:
                        data = response.read().decode("utf-8")
                    root = bs4.BeautifulSoup(data, "html.parser")
                    finding = root.find("th", text = re.compile('members:'))
                    if finding != None:
                        parent_tag = finding.parent
                        find_group_members = parent_tag.find_all("a", href = re.compile('artist'))
                        for member in find_group_members:
                            member_url = member.get('href')
                            member_weights = [member_url]*300
                            features.extend(member_weights)
        elif category == "2": # It's a group
            finding = root.find("th", text = re.compile('members:'))
            if finding != None:
                parent_tag = finding.parent
                find_group_members = parent_tag.find_all("a", href = re.compile('artist'))
                for member in find_group_members:
                    member_url = member.get('href')
                    member_weights = [member_url]*300
                    features.extend(member_weights)
        else: # neither a person nor a group, then what is it?? xd
            pass

        count = Counter(features)
        df1 = pd.DataFrame.from_dict(count, orient='index').reset_index()
        df1 = df1.rename(columns={'index':'related_artist', 0:'weights'})
        row_num = df1.shape[0]
        artist_list = [artist]*row_num
        artist_ = {"artist": artist_list}
        df2 = pd.DataFrame(artist_)
        feat_df = pd.concat([df2, df1], axis=1)
        
        for index in range(feat_df.shape[0]):
            feat_url = feat_df.iloc[index,1]
            url = self.suburl + feat_url
            request=req.Request(url, headers={
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
            })
            with req.urlopen(request) as response:
                data = response.read().decode("utf-8")

            root = bs4.BeautifulSoup(data, "html.parser")
            find_name = root.find("div", class_ = re.compile('artistheader'))
            if find_name != None:
                self.name = find_name.h1.a.bdi.string
                feat_df.iloc[index,1] = self.name
            #time.sleep(random.randint(1,3))
        # Drop if the feature name is the main asrtist herself(himself)
        index_ = feat_df.loc[feat_df['related_artist'] == artist].index.tolist()
        feat_df.drop(index_ , inplace=True)
        return feat_df

class save_csv1():
    def __init__(self):
        self.path = ""

    def write_csv1(self, switch, info, file_num):
        #CHANGE YOUR PATH HERE
        self.path = "/Users/Stephanie/Desktop/pop1_file.csv"
        if switch == 1:
            info.to_csv(self.path, index=False, header=True)
        else:
            info.to_csv(self.path, mode='a', index=False, header=False)

class save_csv2():
    def __init__(self):
        self.path = ""
    
    def write_csv2(self, features_df, switch, file_num):
        #CHANGE YOUR PATH HERE
        self.path = "/Users/Stephanie/Desktop/pop2_file.csv"
        if switch == 1:
            features_df.to_csv(self.path, index=False, header=True)
        else:
            features_df.to_csv(self.path, mode='a', index=False, header=False)


if __name__=='__main__':
    start_time = time.time()

    count_artists = 1
    file_num = 1
    suburl = "https://musicbrainz.org"

    switch_1 = 1 # 1 for starting a new file
    switch_2 = 1
    switch_3 = 1
    
    # 100 artist urls here
    artist_list = dtl.load_urls()


    for artist_URL in artist_list:
        all_albums = []
        albums_urls = []
        artist = ""
        feature_urls = []

        print("Now artist %d ing" % (count_artists))
        artist_URL = suburl + artist_URL
        checkArea = check_area()
        artist_area = checkArea.get_area(artist_URL)

        getAlbumsInfo = get_all_albums_info()
        artist, all_albums, albums_urls, category = getAlbumsInfo.getAlbums(artist_URL)
        for album in all_albums:
            same_album_urls = []
            current_album = ""
            year = ""

            current_album = album
            index = all_albums.index(current_album)
            current_album_url = albums_urls[index]
            #當前album的連結,send進第二層dunction中
            getSameAlbumURLs = get_same_albums_URLs()
            same_album_urls = getSameAlbumURLs.getURLs(current_album_url, artist)
            if same_album_urls != None:
                for same_album in same_album_urls:
                    getSongs = get_Song()
                    year, songs, feat_urls = getSongs.get_Songs(same_album, artist)
                    if feat_urls != None:
                        feature_urls.extend(feat_urls)
                    for song in songs:
                        if switch_1 == 1:
                            information = pd.DataFrame(columns={"country":"","artist":"","date":"","album":"","song":""})
                            switch_1 = 0
                        information.loc[information.shape[0]] = [artist_area, artist, year, current_album, song]
                    #time.sleep(random.randint(1,3))
                    #print("It  is working")
            else:
                getSongs = get_Song()
                year, songs, feat_urls = getSongs.get_Songs(album, artist)
                if feat_urls != None:
                    feature_urls.extend(feat_urls)
                for song in songs:
                    if switch_1 == 1:
                        information = pd.DataFrame(
                            columns={"country": "", "artist": "", "date": "", "album": "", "song": ""})
                        switch_1 = 0
                    information.loc[information.shape[0]] = [artist_area, artist, year, current_album, song]
                # time.sleep(random.randint(1,3))
                # print("It  is working")

            #time.sleep(random.randint(1,3))


        information.drop_duplicates(subset=['artist','song'], keep='first', inplace=True)
            
        file_1 = save_csv1() # Save all the informations (country, artist name, year, album, song)
        file_1.write_csv1(switch_2, information, file_num)
        information.drop(information.index, inplace=True)

        switch_2 = 0
    
        if feature_urls != None: # Check all the related artists
            getFeatures = get_features()
            feats_dataframe = getFeatures.getNames(artist_URL, artist, feature_urls, category) #error

            file_2 = save_csv2() # Save all the related artists
            file_2.write_csv2(feats_dataframe, switch_3, file_num)
            switch_3 = 0

        else:
            pass

        count_artists += 1  # Count how many artists so far
                


            




