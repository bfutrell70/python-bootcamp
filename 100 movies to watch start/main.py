import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"
response = requests.get(URL)

data = response.text

# Write your code below this line 👇
soup = BeautifulSoup(data, 'html.parser')

title_elements = soup.find_all(name='h3', class_='title')
# print(titles)

# titles = []
# for title in title_elements:
#     # print(title.string)
#     titles.append(title.get_text().encode('utf-8'))

titles = [movie.get_text().encode('utf-8') for movie in title_elements]
titles.reverse()
with open('movies.txt', 'w') as file:
    for title in titles:
        file.write(f"{str(title)}\n")
