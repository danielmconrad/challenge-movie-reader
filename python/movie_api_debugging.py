from abc import abstractmethod
from typing import List, Dict
import json

import requests
from requests import Response


class MovieReader:
    url: str = ""

    @abstractmethod
    def get_movies(self, title: str) -> List[Dict]:
        pass

class HackerRankMovieReader(MovieReader):
    def __init__(self):
        self.url = "https://jsonmock.hackerrank.com/api/movies/search/?Title={title}&page={page}"

    def get_movies(self, title: str) -> List[Dict]:
        """
        Returns a list of movies, as dictionaries, that contains the title and date of the movie.
        Example:
            input: title = "movie"

            returns: [{"title": "good movie", "year": 2010}, {"title": "another movie", "year": 2011}]
        """
        page_number: int = 1
        results: List[Dict] = []

        while True:
            response: Response = requests.get(self.url.format(title=title, page=page_number))
            movies = response.json()

            for movie in movies['data']:
                results.append({
                    "title": movie["Title"],
                    "year": movie["Year"],
                })

            if page_number >= movies["total_pages"]:
                break

            page_number += 1

        return results

    def match_movies(self, primary: str, secondary: str) -> Dict:
        """
        Returns a dictionary of movies along with the year(s) of release, that match both the primary
        and secondary terms (case insensitive).  The initial query is performed on the primary term.
        Example:
            input: primary = "movie", secondary = "the"

            returns:
            {
                "The Movie": [1982],
                "Movie of the Year": [1999, 2008]
            }
        """
        secondary_lower = secondary.lower()
        results = {}

        movies = self.get_movies(primary)

        for movie in movies:
            if secondary_lower in movie["title"].lower():
                title = movie['title']
                year = movie['year']
                results[title] = [*results.get(title, []), year]

        return results


def main():

    movie_reader = HackerRankMovieReader()

    # Validation Tests
    with open("movie_api_debugging_testcases.txt") as file:
        for data in file.read().split("\n\n"):
            data = data.split("\n")
            print(f"Running {data[0]}")

            matches = movie_reader.match_movies(data[1].split(" ")[0], data[1].split(" ")[1])
            results = json.dumps(matches, separators=(',', ':'), ensure_ascii=True)

            if (matches == json.loads(data[2])):
                print(f"{data[0]} Passed!\n")
            else:
                print(f"{data[0]} Failed.\nExpected: {data[2]}\nActual: {results}")

if __name__ == "__main__":
    main()
