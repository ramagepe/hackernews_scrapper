# HackerNews Posts Scrapper
Scraps data from HackerNews (https://news.ycombinator.com/) and opens in browser the posts with 100 points or higher in two ways: 

1. Page by page 
2. Selecting the number of posts and pages to scrap 

## Before running
[Install Poetry](https://python-poetry.org/docs/#installation) in your system if not already installed and then run inside the project directory:
```
poetry init
```
This will install all the packages needed to run the script

## Application example
### 1. Page by page 
The execution of the file must be followed by the 'all' flag:
```
poetry run python hackernews_scrapper.py all
```
The 'all' flag will tell the program to open all posts with >100 points, page by page

### 2. By selection
The execution of the file must be followed by the 'best' flag, then the number of posts to show and finally the number of pages to scrap:
```
poetry run python hackernews_scrapper.py best 10 5
```
May be translated to "show me the best 10 posts of the first 5 pages"
