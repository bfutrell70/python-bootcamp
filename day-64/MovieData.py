class MovieData:
    def __init__(self, title, img_url, year, description) -> None:
        self.title:str = title
        self.img_url: str = img_url
        self.year:str = year
        self.description:str = description