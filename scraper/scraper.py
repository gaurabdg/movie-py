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
        """ fetch metadata of movies """

        movie_list = self.connect().find_all('div', class_='lister-item mode-advanced')
        for container in movie_list:
            name = container.h3.a.text
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

# TODO Resolve faulty year data trailing chars

mov = movies(3)
mov.connect()
mov.fetch_data()

dataframe_test = pd.DataFrame({'movie': mov.names,
                       'year': mov.years,
                       'genre': mov.genres,
                       'cast': mov.actors})

dataframe_test.to_csv('dump.csv')
print("{} movies fetched".format(len(mov.names)))


for movie_name in mov.names:
    query_url = urllib.request.urlopen("http://www.yifysubtitles.com/search?q=" + ("+".join(movie_name.split(" "))))
    soup = BS(query_url, "html.parser")

    if not soup.find('div', {'style': 'text-align:center;'}) is None:
        if soup.find('div', {'style': 'text-align:center;'}).text == "no results":
            print("not found 1")
            continue

    result_list = soup.findAll('li', {'class': 'media media-movie-clickable'})
    select_list = BS(str(result_list), "html.parser").findAll('div', {'class': 'media-body'})

    result_url = ""
    for i in range(len(result_list)):
        if movie_name==soup.findAll('h3', {'class': 'media-heading'})[i].text:
            result_url = BS(str(select_list[i]), "html.parser").find('a').get('href')
            break

    html = urllib.request.urlopen("http://www.yifysubtitles.com" + result_url)
    soup = BS(html, "html.parser")
    dict_language_ratings = {}

    flags = BS(str(soup.find('tbody').findAll('td', {'class': 'flag-cell'})), "html.parser")

    for i in range(len(soup.find('tbody').findAll('tr'))):
        if BS(str(flags), "html.parser").findAll('span', {'class': 'sub-lang'})[i].text == "English":
            dict_language_ratings[BS(str(soup.find('tbody').findAll('td', {'class': 'rating-cell'})), "html.parser").findAll('span')[i].text] = i

    if dict_language_ratings == {}:
        print("not found 2")
        continue


    dict_language_ratings = {int(v): int(k) for k, v in dict_language_ratings.items()}
    i = max(dict_language_ratings, key=dict_language_ratings.get)
    url = BS(str(soup.find('tbody').findAll('td', {'class': 'download-cell'})), "html.parser").findAll('a', attrs={'href': re.compile("/subtitles/")})[i].get('href')

    html = urllib.request.urlopen("http://www.yifysubtitles.com" + url)
    soup = BS(html, "html.parser")
    url = soup.find('a', {'class': 'btn-icon download-subtitle'}).get('href')

    urllib.request.urlretrieve(url, "subtitle.zip")
    target_zip = ZipFile("subtitle.zip")
    target_zip.extractall()
    target_zip.close()
    os.remove("subtitle.zip")
    print("done")

    # exec_int("Downloaded and Renamed")

