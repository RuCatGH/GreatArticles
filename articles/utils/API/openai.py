import re
import markdown
import random
import time

from openai.error import ServiceUnavailableError, RateLimitError
import openai
import os
from dotenv import load_dotenv
from translate import Translator

from articles.models import Category, Article
from articles.utils.prompts import (
    prompt_create_headings_table, prompt_create_description, prompt_create_article,
    prompt_get_img, prompt_check_img
)

load_dotenv()

openai.api_key = os.getenv('OPEN_API_KEY')


def create_article(topic: str) -> tuple[str, str, str, str, str]:
    try:
        for _ in range(3):
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt_create_headings_table.format(topic)}
                ]
            )
            plan = completion.choices[0].message.content

            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=[
                    {"role": "assistant", "content": plan},
                    {"role": "assistant", "content": prompt_create_article}
                ]
            )

            article_text = completion.choices[0].message.content

            pattern = r'#.*?\n(.*)'
            match = re.search(pattern, article_text, re.DOTALL)

            article_content = markdown.markdown(match.group(1)).replace('<p>Введение</p>', '', 1).replace(
                '<h2>Введение</h2>', '', 1).replace('h1', 'h2').replace(
                '<h3>Введение</h3>', '', 1).replace('(H1)', '').replace('(H2)', '').replace('(H3)', '').replace('(H4)', '')

            if article_content.count('<h2>') >= 3:
                break

        pattern = r'# (.*)'
        title = re.search(pattern, article_text).group(1)

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "assistant", "content": article_content},
                {"role": "user", "content": prompt_create_description},
            ]
        )

        description = completion.choices[0].message.content.replace('"', '')
        description = description[:description.rfind('.')]

        categories = list(Category.objects.all())
        category_names = [category.name for category in categories]

        prompt_choose_category = (
            f'Of all the categories {",".join(category_names)} choose the appropriate one for this article. '
            'You only have to choose from the categories provided. You should just capitalize the category '
            'without dots or other symbols, just the word. If there is nothing suitable, choose at least '
            'some indirectly related category. Dont change the ending. For example, if the article is written about travel, you should write Путешествие. If there is no appropriate topic write Образование'
        )

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "assistant", "content": title},
                {"role": "user", "content": prompt_choose_category},
            ]
        )

        category = completion.choices[0].message.content.replace('.', '').replace("'", '')

        query_keyword = create_keywords_for_image(article_content)
    except ServiceUnavailableError:
        delay = 2 ** random.randint(0, 5)  # Генерация случайной задержки от 1 до 32 секунд
        time.sleep(delay)
        return create_article(topic)
    except RateLimitError:
        time.sleep(30)
        return create_article(topic)
    return article_content, description, category, title, query_keyword


def create_titles_for_articles(n: int) -> str:
    titles_article = list(Article.objects.all())
    titles = [title.article_title for title in titles_article]
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "assistant", "content": '|'.join(titles[:len(titles)//6])},
            {"role": "user", "content": f'Не повторяя эти темы, то есть не должно быть одинаковых тем про одно и тоже напиши ещё {n} интересных и полезных тем. Перечисля темы через |'},
        ]
    )

    titles = completion.choices[0].message.content.replace('.', '').replace("'", '')

    return titles


def create_keywords_for_image(article: str) -> str:
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "assistant", "content": article},
                {"role": "user", "content": prompt_get_img},
            ]
        )
        prompt = completion.choices[0].message.content
        translator = Translator(from_lang='ru', to_lang="en")
        translation = translator.translate(prompt)
        return translation
    except RateLimitError:
        time.sleep(30)
        return create_keywords_for_image(article)
    except ServiceUnavailableError:
        delay = 2 ** random.randint(0, 5)  # Генерация случайной задержки от 1 до 32 секунд
        time.sleep(delay)
        return create_keywords_for_image(article)


def check_relevant_img(alt_description, title) -> bool:
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "assistant", "content": f'Title: {title}, Description img {alt_description}'},
                {"role": "user", "content": prompt_check_img},
            ]
        )
        check_answer = completion.choices[0].message.content

        if 'yes' in check_answer.lower():
            return True
        else:
            return False
    except RateLimitError:
        time.sleep(30)
        return check_relevant_img(alt_description, title)
    except ServiceUnavailableError:
        delay = 2 ** random.randint(0, 5)  # Генерация случайной задержки от 1 до 32 секунд
        time.sleep(delay)
        return check_relevant_img(alt_description, title)

