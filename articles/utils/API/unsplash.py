import os
import random

import requests
from dotenv import load_dotenv

from articles.utils.API.openai import check_relevant_img, create_keywords_for_image

load_dotenv()

UNSPLASH_KEY = os.getenv('UNSPLASH_API_KEY')


def get_img_from_keyword(keyword: str, title: str, n=0) -> str:
    n += 1
    api_url = 'https://api.unsplash.com/search/photos'
    params = {'query': keyword, 'order_by': 'relevant', 'client_id': UNSPLASH_KEY}

    response = requests.get(api_url, params=params, allow_redirects=True)
    img_json = response.json()
    random_int = random.randint(0, len(img_json['results']) - 1)
    url_img = img_json['results'][random_int]['urls']['regular']
    description = img_json['results'][random_int]['alt_description']

    if check_relevant_img(description, title) or n == 10:
        return url_img
    else:
        keyword = create_keywords_for_image(title)
        return get_img_from_keyword(keyword, title, n)
