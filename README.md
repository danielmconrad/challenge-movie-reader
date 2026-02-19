# Welcome to Infinia MLs take home coding challenge!

This is an exercise designed to grasp your ability to reason about and understand an existing codebase. The code presented has numerous bugs to fix, and the expected behavior is documented below for you. Additionally, unit tests exist to help you identify and fix the bugs. When all of the tests pass, you have completed the assignment.

You can solve the problem in either Python or Javascript and plan to work within the appropriate file.

Please try to time box yourself to 90 minutes. Good luck!

## Installation

If using the javascript version of this test:

- npm install
- npm run test

## Requirements

The application below is meant to find similarly titled movies from a remote database.
The search method takes two parameters, the primary term to search for, and a secondary term to filter the results on.
The resultant data should be a dictionary of movie titles, with each entity containing a list of all the years that particular title was released.
The search should be case-insensitive.

### Example

Input:
["Walk", "The"]

Output:
{
"The Walk": [1999, 2008],
"Walking through the Park": [2021],
"The Walks that made us": [1945, 1976, 2001, 2019],
}

## Additional API Information

In the code to get the data we make an API GET call to the URL 'https://jsonmock.hackerrank.com/api/movies/search/?Title={title}&page={page}'.

The response to such a request is a JSON record with the following 5 fields:

page: the current page of the results
per_page: the maximum number of results returned per page
total: the total number of results
total_pages: the total number of pages with results
data: an array of objects containing the desired data. Each object is a movie record having the below schema:
Title - Movie title
Year - Movie year (same as the year that was queried)
imdbID - Movie ID

Here is an example of a movie record:

{
"Title": "Harry & Snowman",
"Year": 2015,
"imdbID": "tt2898306"
}
