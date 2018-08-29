from requests import get
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.imdb.com/search/title?count=50&groups=top_1000&sort=num_votes'
response = get(url)
# print(response.text[:500])
html_soup = BeautifulSoup(response.text, 'html.parser')
movie_list = html_soup.find_all('div', class_='lister-item mode-advanced')
# print(len(movie_list))
# first_movie = movie_list[0]
# first_name = first_movie.h3.a.text
# print(first_name)
# stringex = first_movie.find('span', class_ = 'lister-item-year text-muted unbold').text
# stringex = stringex.strip("()")
# print(stringex)
# print(first_movie.find('div', class_ = 'lister-item-content').find('p', class_ ='text-muted').find('span', class_ = 'genre').text)
# actor = ""
# for i in range(1,5):
#     actor += (first_movie.find_all('p')[2].find_all('a')[i].text+", ")
# print(actor)

names = []
years = []
genres = []
actors = []

for container in movie_list:
    name = container.h3.a.text
    names.append(name)

    year = container.find('span', class_ = 'lister-item-year text-muted unbold').text
    year = year.strip("()")
    years.append(year)

    genre = container.find('div', class_ = 'lister-item-content').find('p', class_ ='text-muted').find('span', class_ = 'genre').text
    genre = genre.strip("\n")
    genres.append(genre)

    actor = ""
    for i in range(1,5):
        actor += (container.find_all('p')[2].find_all('a')[i].text+", ")
    actors.append(actor)


dataframe_test = pd.DataFrame({'movie': names,
                       'year': years,
                       'genre': genres,
                       'cast': actors})
print(dataframe_test.values)


