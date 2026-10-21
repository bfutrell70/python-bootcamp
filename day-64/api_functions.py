import requests
import os
from dotenv import load_dotenv
from MovieData import MovieData

class APIFunctions():
    def __init__(self):
        load_dotenv()
        self.api_read_token = os.environ['API_READ_ACCESS_TOKEN']
        self.search_url = 'https://api.themoviedb.org/3/search/movie'
        self.detail_url = 'https://api.themoviedb.org/3/movie/'
        self.image_url = "https://image.tmdb.org/t/p/original"

    def search_for_movies(self, search_text:str):
        page_number = 1
        max_page_number = 1
        next_page = True
        movies:list[MovieData] = []

        custom_headers = {
            "Authorization": f"Bearer {self.api_read_token}"
        }

        while next_page:
            print(f"in loop, page number {page_number}")

            parameters = {
                "query": search_text,
                "page": page_number
            }

            response = requests.get(url=self.search_url, headers=custom_headers, params=parameters)
            if response.status_code == 200:
                movie_data = response.json()
                max_page_number = movie_data["total_pages"]
        
                for movie in movie_data["results"]:
                    m = MovieData(
                        title= movie["title"],
                        img_url= '',
                        year= movie["release_date"],
                        description= movie["overview"],        
                    )
                    if movie["poster_path"]:
                        m.img_url = f"{self.image_url}{movie["poster_path"]}"
                    else:
                        m.img_url = f"{self.image_url}/None"

                    movies.append(m)

                # see if there is another page to retrieve
                if page_number == max_page_number:
                    next_page = False
                else:
                    page_number = page_number + 1
            else:
                # an error occurred when making the API call
                next_page = False

        return movies

    def get_movie_detail(self, movie_id:int):
        pass
