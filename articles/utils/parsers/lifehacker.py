from bs4 import BeautifulSoup
import requests


def get_titles_from_site(url: str) -> str:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    titles = [title.text for title in soup.find_all('div', class_='lh-small-article-card__title')]
    return '|'.join(titles)