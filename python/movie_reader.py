from abc import abstractmethod

import requests
from pydantic import AliasChoices, BaseModel, Field
from requests import Response

MOVIE_SEARCH_BASE_URL = "https://jsonmock.hackerrank.com/api/movies/search"


class Movie(BaseModel):
    title: str = Field(validation_alias=AliasChoices("title", "Title"))
    year: int = Field(validation_alias=AliasChoices("year", "Year"))


class MoviesResponsePage(BaseModel):
    data: list[Movie]
    page: int
    per_page: int
    total_pages: int
    total: int

    @property
    def last_page(self) -> bool:
        return self.page == self.total_pages


class MovieReader:
    url: str = ""

    @abstractmethod
    def get_movies(self, title: str) -> list[dict]:
        pass


class HackerRankMovieReader(MovieReader):
    url = "{base_url}/?Title={title}&page={page}"

    def match_movies(self, search_term: str, filter_term: str) -> dict[str, list[int]]:
        """
        Returns a dictionary of movies along with the year(s) of release, that
        match both the search_term and filter_term (case insensitive).
        The initial query is performed on the search_term.

        Example:
            input:      search_term = "movie", filter_term = "the"
            returns:    {"The Movie": [1982], "Movie of the Year": [1999, 2008]}
        """
        filter_term_lower = filter_term.lower()
        results = {}

        movies = self._get_movies(search_term)

        for movie in movies:
            if filter_term_lower in movie.title.lower():
                results[movie.title] = [*results.get(movie.title, []), movie.year]

        return results

    def _get_movies(self, title: str) -> list[Movie]:
        page_number: int = 1
        results: list[Movie] = []

        while True:
            url = self.url.format(
                base_url=MOVIE_SEARCH_BASE_URL, title=title, page=page_number
            )
            response_json: Response = requests.get(url).json()
            response_page = MoviesResponsePage.model_validate(response_json)

            for movie in response_page.data:
                results.append(movie)

            if response_page.last_page:
                break

            page_number += 1

        return results
