import axios from "axios";
import testCases from "./movie_api_debugging_testcases.js";

class HackerRankMovieReader {
  constructor() {
    this.url = "https://jsonmock.hackerrank.com/api/movies/search";
  }

  getUrl({ title, page }) {
    return `${this.url}/?Title=${title}&page=${page}`;
  }

  /**
   * Returns an array of movies, as objects, that contains the title and date of
   * the movie containing the exact searchTerm
   *
   * Example:
   *  input: title = "movie"
   *
   *  returns:
   *      [
   *          { title: "good movie", year: 2010 },
   *          { title: "another movie", year: 2011 }
   *      ]
   */
  async getMovies(title) {
    let page = 1;
    const results = [];
    let url = this.getUrl({ title, page });

    while (true) {
      url = this.getUrl({ title, page });
      const response = await axios.get(url);
      const movies = response.data.data;

      for (let movie in movies) {
        results.push({
          Title: movies[movie].Title,
          Year: movies[movie].Year,
        });
      }

      page += 1;
      if (page > response.data.total_pages) break;
    }

    return results;
  }

  /**
   * Returns an object with movie titles as the key, and an array with the year(s)
   * of release as the value. These match both the primary and secondary terms
   * exactly (case insensitive). The initial query is performed on the primary term.
   *
   * Example:
   *  input: primary = "movie", secondary = "the"
   *
   *  returns:
   *      {
   *         "The Movie": [1982],
   *          "Movie of the Year": [1999, 2008]
   *      }
   */
  async matchMovies(primaryTerm, secondaryTerm) {
    const results = {};
    const movies = await this.getMovies(secondaryTerm);

    for (let movie of movies) {
      if (movie.Title.toLowerCase().includes(secondaryTerm.toUpperCase())) {
        results[movie.Title] = [movie.Year];
      }
    }
    return results;
  }
}

async function processData({ name, primaryTerm, secondaryTerm, expected }) {
  const movieReader = new HackerRankMovieReader();

  const matches = await movieReader.matchMovies(primaryTerm, secondaryTerm);

  if (JSON.stringify(matches) == JSON.stringify(expected)) {
    console.log(`${name}: PASSED`);
  } else {
    console.log(`${name}: FAILED`);
    console.log(`Expected: ${JSON.stringify(expected)}`);
    console.log(`Actual: ${JSON.stringify(matches)}\n`);
  }
}

async function runTestCases() {
  for (const testCase of testCases) {
    await processData(testCase);
  }
}

runTestCases();
