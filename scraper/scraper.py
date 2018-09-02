""" Dependencies """

from requests import get
from bs4 import BeautifulSoup as BS
import pandas as pd
from zipfile import ZipFile
import urllib.request
import os
import re
import time

def exec_int(msg):
    print(msg)
    time.sleep(2)
    exit()

class movies:
    """ class for fetching movie metadata """

    names = []
    years = []
    genres = []
    actors = []
    number_movies = 0
    movie_list = ""

    def __init__(self, number_movies):
        """ specify number of movies to fetch """

        self.number_movies = number_movies

    def connect(self):
        """ establish connection with IMDB website and create beautiful soup object for parsing retrieved html document """

        url = 'https://www.imdb.com/search/title?count={}&groups=top_1000&sort=num_votes'.format(self.number_movies)
        response = get(url)
        html_soup = BS(response.text, 'html.parser')
        return html_soup

    def fetch_data(self):
        """ fetch metadata of movies and invoke subtitle fetching utility with name and year parameters """

        movie_list = self.connect().find_all('div', class_='lister-item mode-advanced')
        for container in movie_list:
            name = container.h3.a.text
            if name.isascii() is True:
                movies.names.append(name)

            year = container.find('span', class_='lister-item-year text-muted unbold').text
            year = year.strip("()")
            movies.years.append(year)

            genre = container.find('div', class_='lister-item-content').find('p', class_='text-muted').find('span', class_='genre').text
            genre = genre.strip()
            movies.genres.append(genre)

            actor = ""
            for i in range(1, 5):
                actor += (container.find_all('p')[2].find_all('a')[i].text + ", ")
            movies.actors.append(actor)

            #problem with unicode
            if name.isascii() is True:
                print("{} is being processed".format(name))
                # searchfilename = name.strip()
                searchfilename = name + ".srt"
                if os.path.isfile(searchfilename) is False:
                    fetch_subtitle(name, year)


# TODO Resolve faulty year data trailing chars

def fetch_subtitle(movie_name, movie_year):
    """ Scraping YIFY subtitles """

    # search for the given movie
    query_url = urllib.request.urlopen("http://www.yifysubtitles.com/search?q=" + ("+".join(movie_name.split(" "))))
    soup = BS(query_url, "html.parser")

    # check if subtitles available for the given movie
    if not soup.find('div', {'style': 'text-align:center;'}) is None:
        if soup.find('div', {'style': 'text-align:center;'}).text == "no results":
            print("{} not found".format(movie_name))
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
                return
            continue

    if result_url is None:
        print("result url absent")

    # opening the page for the selected result
    html = urllib.request.urlopen("http://www.yifysubtitles.com" + result_url)
    soup = BS(html, "html.parser")

    # processing the available subtitles list to retrieve the file with lang=ENG and with MAX VOTES
    dict_language_ratings = {}

    flags = BS(str(soup.find('tbody').findAll('td', {'class': 'flag-cell'})), "html.parser")

    for i in range(len(soup.find('tbody').findAll('tr'))):
        if BS(str(flags), "html.parser").findAll('span', {'class': 'sub-lang'})[i].text == "English":
            dict_language_ratings[
                BS(str(soup.find('tbody').findAll('td', {'class': 'rating-cell'})), "html.parser").findAll('span')[
                    i].text] = i

    if dict_language_ratings == {}:
        print("english sub not found")

    dict_language_ratings = {int(v): int(k) for k, v in dict_language_ratings.items()}
    i = max(dict_language_ratings, key=dict_language_ratings.get)
    url = BS(str(soup.find('tbody').findAll('td', {'class': 'download-cell'})), "html.parser").findAll('a', attrs={
        'href': re.compile("/subtitles/")})[i].get('href')

    # downloading the subtitle zip
    html = urllib.request.urlopen("http://www.yifysubtitles.com" + url)
    soup = BS(html, "html.parser")
    url = soup.find('a', {'class': 'btn-icon download-subtitle'}).get('href')
    urllib.request.urlretrieve(url, "subtitle.zip")

    # extracting the zip, renaming the file and deleting the zip
    target_zip = ZipFile("subtitle.zip")
    subname = target_zip.namelist()[0]
    target_zip.extractall()
    target_zip.close()
    os.remove("subtitle.zip")
    fname = movie_name.strip()
    os.rename(subname, fname + ".srt")

    print("{} download done".format(movie_name))
    time.sleep(1)

mov = movies(50)
mov.connect()
mov.fetch_data()

# dataframe_test = pd.DataFrame({'movie': mov.names,
#                        'year': mov.years,
#                        'genre': mov.genres,
#                        'cast': mov.actors})
#
# dataframe_test.to_csv('dump.csv')
# print("{} movies fetched".format(len(mov.names)))

# exec_int("Downloaded and Renamed")

