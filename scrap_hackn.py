"""
Scraps data from HakerNews to open in browser only
the posts with 100 points or higher, page by page
and log filtered data in the terminal.
"""

import webbrowser
from sys import argv
import requests
from bs4 import BeautifulSoup
from rich import print as printr


def filter_news(response):
    """Resturns a list of all posts with 100 points or higher"""
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = clean_titles(soup.select('td:nth-child(3) > .titleline > a'))
    links = clean_links(soup.select('td:nth-child(3) > .titleline > a'))
    scores = clean_scores(soup.select('.score'))
    return package_data(titles, links, scores)


def clean_titles(titles):
    """Cleans scrapped post titles"""
    return [title.string for title in titles]


def clean_links(links):
    """Cleans scrapped post links"""
    return [link['href'] for link in links]


def clean_scores(scores):
    """Cleans scrapped post scores"""
    return [int(score.string[:score.string.find(' ')])
            for score in scores]


def package_data(titles, links, scores):
    """Recieves 3 cleaned types of data and chunk them into a curated list

    Args:
        titles (list): list of post titles
        links (list): list of post links
        scores (list): list of post scores

    Returns:
        list: a list of dictionaries, each of them containing the three passed args
    """
    floor = 99
    curated_lst = []
    for title, link, score in zip(titles, links, scores):
        if score > floor:
            curated_lst.append({'title': title, 'link': link, 'votes': score})
    return curated_lst


def sort_data(packaged_data):
    """Sorts the curated data from higher to lower votes"""
    return sorted(packaged_data, key=lambda x: x['votes'], reverse=True)


def log_scrapping(current_post):
    """Logs in terminal the posts being open by the browser"""
    title, votes = current_post['title'], current_post['votes']
    printr(
        f'[bold white]>>[/bold white] [bold blue]{title}[/bold blue] --> {votes} votes')


def page_by_page():
    """Wrapper function that allows to scrap page by page"""
    page_num = 1
    while True:
        if page_num != 1:
            user_input = input('Filter next page? (y/N): ')
            if user_input != 'y':
                break
        res = requests.get(f'https://news.ycombinator.com/news?p={page_num}')
        data_list = sort_data(filter_news(res))
        for post in data_list:
            webbrowser.open(post['link'])
            log_scrapping(post)
        page_num += 1


def many_sorted(num_posts: int, last_page: int):
    """Wrapper function that shows a given amount of posts from a given amount of pages

    Args:
        num_posts (int): number of posts to return
        last_page (int): number of pages to scrap
    """
    current_page = 1
    data_list = []
    while current_page <= last_page:
        res = requests.get(
            f'https://news.ycombinator.com/news?p={current_page}')
        data_list += filter_news(res)
        current_page += 1
    data_list = sort_data(data_list)
    for i in range(num_posts+1):
        webbrowser.open(data_list[i]['link'])
        log_scrapping(data_list[i])


def log_error():
    """Logs message into the console in case an error occurs"""
    print('\n>> ERROR: Invalid flags')
    print('\n\tall --> shows page by page')
    print(
        '\tbest [num of posts] [num of pages] --> shows top [num of posts] from [num of pages] pages')
    print('\n\tExample 1 >> python scrap_hackn.py all')
    print('\tExample 2 >> python scrap_hackn.py best 10 5')


if __name__ == '__main__':
    try:
        mode = argv[1]
        if mode == 'all':
            page_by_page()
        elif mode == 'best':
            try:
                top_best, num_pages = argv[2], argv[3]
                many_sorted(int(top_best), int(num_pages))
            except IndexError:
                log_error()
        else:
            log_error()
    except IndexError:
        log_error()
    except ValueError:
        log_error()
