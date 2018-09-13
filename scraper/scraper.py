""" Dependencies """

from bs4 import BeautifulSoup as BS
import pandas as pd
from zipfile import ZipFile
from zipfile import BadZipFile
from http.cookiejar import CookieJar
import urllib.error
import urllib.request
import os
import re
import time
import locale
import sys
import subscene

# locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')
# reload(sys)
# sys.setdefaultencoding('utf8')
not_downloaded = []

def exec_int(msg):
    print(msg)
    time.sleep(2)
    exit()

# request headers
cj = CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
user_agent = 'Mozilla/5.0 (Windows NT 6.1; rv:54.0) Gecko/20100101 Firefox/54.0'
opener.addheaders = [('user-agent', user_agent),('Accept-Charset', 'utf-8')]



class movies:
    """ class for fetching movie metadata """

    names = []
    years = []
    genres = []
    actors = []
    director = []
    number_movies = 0
    movie_list = ""

    def __init__(self, number_movies):
        """ specify number of movies to fetch """

        self.number_movies = number_movies

    def connect(self):
        """ establish connection with IMDB website and create beautiful soup object for parsing retrieved html document """

        url = 'https://www.imdb.com/search/title?count={}&groups=top_1000&sort=num_votes'.format(self.number_movies)
        response = opener.open(url)
        html_soup = BS(response, 'html.parser')
        return html_soup

    def fetch_data(self):
        """ fetch metadata of movies and invoke subtitle fetching utility with name and year parameters """

        movie_list = self.connect().find_all('div', class_='lister-item mode-advanced')
        print("connected")
        for container in movie_list:
            name = container.h3.a.text
            print(name)
            # problem with unicode
            if name.isascii() is True:
                movies.names.append(name)

                year = container.find('span', class_='lister-item-year text-muted unbold').text
                year = year.strip("()")
                movies.years.append(year)

                genre = container.find('div', class_='lister-item-content').find('p', class_='text-muted').find('span', class_='genre').text
                genre = genre.strip()
                movies.genres.append(genre)
                self.append_attributes(name,genre)

                actor = ""
                for i in range(1, 5):
                    actor += (container.find_all('p')[2].find_all('a')[i].text + ", ")
                movies.actors.append(actor)
                self.append_attributes(name, actor)

                print("{} is being processed".format(name))
                # searchfilename = name.strip()
                searchfilename = name + ".srt"
                # if os.path.isfile("data/"+searchfilename) is False:
                #     fetch_subtitle(name, year)

            else:
                not_downloaded.append(name)


# TODO Resolve faulty year data trailing chars

    def fetch_subtitle(movie_name, movie_year):
        """ Scraping YIFY subtitles """

        # search for the given movie

        try:
            query_url = opener.open("http://www.yifysubtitles.com/search?q=" + ("+".join(movie_name.split(" "))))
        except urllib.error.HTTPError as err:
            print(err.code)
            not_downloaded.append(movie_name)
            return
        soup = BS(query_url, "html.parser")

        # check if subtitles available for the given movie

        if not soup.find('div', {'style': 'text-align:center;'}) is None:
            if soup.find('div', {'style': 'text-align:center;'}).text == "no results":
                print("{} not found".format(movie_name))
                not_downloaded.append(movie_name)
                return

        # list of all the search returns

        result_list = soup.findAll('li', {'class': 'media media-movie-clickable'})
        select_list = BS(str(result_list), "html.parser").findAll('div', {'class': 'media-body'})

        # processing the list and choosing, if present, the most relevant one wrt movie name or year

        result_url = ""
        for i in range(len(result_list)):
            extracted_moviename = soup.findAll('h3', {'class': 'media-heading'})[i].text
            souptemp = soup.findAll('span', {'class': 'movinfo-section'})[i]
            for tag in souptemp.find_all():
                tag.decompose()
            extracted_year = souptemp.text
            if extracted_moviename == movie_name or extracted_year == movie_year:
                result_url = BS(str(select_list[i]), "html.parser").find('a').get('href')
                break
            else:
                print("not this one")
                if i == (len(result_list)-1):
                    not_downloaded.append(movie_name)
                    return
                continue

        if result_url is None:
            print("result url absent")

        # opening the page for the selected result

        try:
            html = opener.open("http://www.yifysubtitles.com" + result_url)
        except urllib.error.HTTPError as err:
            print(err.code)
            not_downloaded.append(movie_name)
            return
        soup = BS(html, "html.parser")

        # processing the available subtitles list to retrieve the file with lang=ENG and with MAX VOTES

        dict_language_ratings = {}

        if soup.find('tbody') is not None:
            flags = BS(str(soup.find('tbody').findAll('td', {'class': 'flag-cell'})), "html.parser")
        else:
            not_downloaded.append(movie_name)
            return

        for i in range(len(soup.find('tbody').findAll('tr'))):
            if BS(str(flags), "html.parser").findAll('span', {'class': 'sub-lang'})[i].text == "English":
                dict_language_ratings[
                    BS(str(soup.find('tbody').findAll('td', {'class': 'rating-cell'})), "html.parser").findAll('span')[
                        i].text] = i

        if dict_language_ratings == {}:
            print("english sub not found")

        dict_language_ratings = {int(v): int(k) for k, v in dict_language_ratings.items()}
        if len(dict_language_ratings) is not 0:
            i = max(dict_language_ratings, key=dict_language_ratings.get)
        else:
            not_downloaded.append(movie_name)
            return
        url = BS(str(soup.find('tbody').findAll('td', {'class': 'download-cell'})), "html.parser").findAll('a', attrs={
            'href': re.compile("/subtitles/")})[i].get('href')

        # downloading the subtitle zip

        try:
            html = opener.open("http://www.yifysubtitles.com" + url)
        except urllib.error.HTTPError as err:
            print(err.code)
            not_downloaded.append(movie_name)
            return
        soup = BS(html, "html.parser")
        url = soup.find('a', {'class': 'btn-icon download-subtitle'}).get('href')

        try:
            urllib.request.urlretrieve(url, "subtitle.zip")
        except urllib.error.HTTPError as err:
            print(err.code)
            not_downloaded.append(movie_name)
            return

        # extracting the zip, renaming the file and deleting the zip
        try:
            target_zip = ZipFile("subtitle.zip")
        except BadZipFile:
            not_downloaded.append(movie_name)
            return
        subname = target_zip.namelist()[0]
        target_zip.extractall()
        target_zip.close()
        os.remove("subtitle.zip")
        fname = movie_name.strip()
        try:
            os.rename(subname, fname + ".srt")
        except FileNotFoundError:
            not_downloaded.append(movie_name)
            pass


        print("{} download done".format(movie_name))
        print(len(mov.names))
        time.sleep(2)

    def append_attributes(self,filename,content):
        filename = filename+".txt"
        print(filename)
        try:
            with open(os.path.join('data_txt_test/', filename), "a") as f:
                f.write(content+"\n")
        except FileNotFoundError:
            not_downloaded.append(filename)


# scrape for top 1000 IMDB movies
mov = movies(1000)
mov.connect()
mov.fetch_data()

print("*****************")

# with open("not_downloaded.txt", "w") as output:
#     output.write(str(not_downloaded))
#
# print("{} not downloaded".format(len(not_downloaded)))
# # print("{} movies fetched".format(len(mov.names)))
#
# dataframe_test = pd.DataFrame({'movie': mov.names,
#                        'year': mov.years,
#                        'genre': mov.genres,
#                        'cast': mov.actors})
#
# dataframe_test.to_csv('dump.csv')

exec_int("Downloaded and Renamed")

# Download remaining movies from subscene.com
# mov_list = []
# with open("not_downloaded.txt", "r") as file:
#     lines = file.read().split(",")
#
# for line in lines:
#     line = line.replace("'","")
#     line = line.strip()
#     mov_list.append(line)
#
# # print(mov_list)
# subs = []
# for mov in mov_list:
#         film = subscene.search(mov)
#         sub = film.subtitles[42]
#         subs.append(sub.url)
#
# print(subs)





