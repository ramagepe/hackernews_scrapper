"""
Scraps data from HakerNews to open in browser only
the posts with 100 points or higher, page by page
and log filtered data in the terminal.
"""

from curses.panel import top_panel
from dataclasses import dataclass
import webbrowser
import requests
from bs4 import BeautifulSoup
from rich import print as printr
from sys import argv


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
    floor = 99
    curated_lst = []
    for i, score in enumerate(scores):
        if score > floor:
            curated_lst.append({'title': titles[i], 'link': links[i], 'votes': score})
    return curated_lst

def sort_data(packaged_data):
    return sorted(packaged_data, key=lambda x: x['votes'], reverse=True)

def log_scrapping(current_post):
    title, votes = current_post['title'], current_post['votes']
    printr(f'[bold white]>>[/bold white] [bold blue]{title}[/bold blue] --> {votes} votes')

def page_by_page():
    page_num = 1
    while True:
        if page_num != 1:
            user_input = input('Filter next page? (y/N): ')
            if user_input != 'y':
                break
        res = requests.get(f'https://news.ycombinator.com/news?p={page_num}')
        data_list = sort_data(filter_news(res))
        for post in data_list:
            # webbrowser.open(post['link'])
            log_scrapping(post)
        page_num += 1

def many_sorted(num_posts:int, last_page:int):
    current_page = 1
    data_list = []
    while current_page <= last_page:
        res = requests.get(f'https://news.ycombinator.com/news?p={current_page}')
        data_list += filter_news(res)
        current_page += 1
    data_list = sort_data(data_list)
    for i in range(1, num_posts+1):
        # webbrowser.open(data_list[i]['link'])
        log_scrapping(data_list[i])

def log_error():
    print('\n>> ERROR: Invalid flags')
    print('\n\tall --> shows page by page')
    print('\tbest [num of posts] [num of pages] --> shows top [num of posts] from [num of pages] pages')
    print('\n\tExample 1 >> python scrap_hackn.py all')
    print('\tExample 2 >> python scrap_hackn.py best 5')

if __name__ == '__main__':
    try:
        mode, top_best, num_pages = argv[1:]
        if mode == 'all':
            page_by_page()
        elif mode == 'best':
            many_sorted(int(top_best), int(num_pages))
        else:
            log_error()
    except IndexError:
        log_error()
    except ValueError:
        log_error()
