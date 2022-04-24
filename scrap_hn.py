"""
Scraps data from HakerNews to open in browser only
the posts with 100 points or higher, page by page
and log filtered data in the terminal.
"""

import webbrowser
import requests
from bs4 import BeautifulSoup
from rich import print as printr


def filter_news(response):
    """Resturns a list of post links with 100 points or higher"""

    soup = BeautifulSoup(response.text, 'html.parser')
    titles = clean_titles(soup.select('.titlelink'))
    links = clean_links(soup.select('.titlelink'))
    scores = clean_scores(soup.select('.score'))
    return package_data(titles, links, scores)

def clean_titles(titles):
    return [title.string for title in titles]

def clean_links(links):
    return [link['href'] for link in links]

def clean_scores(scores):
    return [int(score.string[:score.string.find(' ')])
                 for score in scores]

def package_data(titles, links, scores):
    curated_lst = []
    for i, score in enumerate(scores):
        if score > 100:
            curated_lst.append({'title': titles[i], 'link': links[i], 'votes': score})
    return curated_lst

def log_scrapping(current_post):
    title, votes = current_post['title'], current_post['votes']
    printr(f'[bold white]>>[/bold white] [bold blue]{title}[/bold blue] --> {votes} votes')


if __name__ == '__main__':
    page_num = 1

    while True:
        if page_num != 1:
            user_input = input('Filter next page? (y/N): ')
            if user_input != 'y':
                break
        res = requests.get(f'https://news.ycombinator.com/news?p={page_num}')
        for post in filter_news(res):
            webbrowser.open(post['link'])
            log_scrapping(post)
        page_num += 1
