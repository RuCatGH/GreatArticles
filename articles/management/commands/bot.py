import io
import os
import time

from django.core.files import File
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
import telebot
from telebot.types import Message
from pytils.translit import slugify
from openai.error import APIError
import requests
from PIL import Image

from articles.utils.API.openai import create_article, create_titles_for_articles
from articles.utils.API.unsplash import get_img_from_keyword
from articles.utils.keyboards.admin import admin_kb_start, make_row_keyboard, admin_kb_choose_topic
from articles.utils.parsers.lifehacker import get_titles_from_site
from userprofile.models import CustomUser
from django.utils import timezone
from articles.models import Article, Category

load_dotenv()

bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))


def download_image_from_url(image_url: str) -> bytes:
    response = requests.get(image_url)
    response.raise_for_status()
    return response.content


def create_django_file_from_bytes(image_bytes: bytes) -> File:
    return File(io.BytesIO(image_bytes))


def convert_image_to_webp(image_bytes: bytes) -> bytes:
    image = Image.open(io.BytesIO(image_bytes))
    resized_image = image.resize((837, 637))
    output_buffer = io.BytesIO()
    resized_image.save(output_buffer, format='WebP')
    return output_buffer.getvalue()


def send_article_photo(message: Message, django_file: File):
    bot.send_photo(chat_id=message.chat.id, photo=django_file, reply_markup=make_row_keyboard(admin_kb_choose_topic))


def create_article_with_image(
        title: str, user: CustomUser, description: str, article: str, slug: str,
        category: Category, image_filename: str, django_file: File
):
    article = Article(
        article_author=user,
        article_title=title,
        description=description,
        header_background='linear-gradient(to bottom, #fff 0%, #fff 100%)',
        article_text=article,
        pub_date=timezone.now().date(),
        slug=slug,
        category=category,
        article_image=None,
        keywords='',
        is_published=True,
    )
    image_filename_webp = os.path.splitext(image_filename)[0] + '.webp'
    article.article_image.save(image_filename_webp, django_file)
    article.save()


@bot.message_handler(commands=['admin'])
def admin_mode(msg: Message):
    if msg.from_user.id == 701151229:
        bot.send_message(msg.chat.id, '📟 Панель администратора', reply_markup=admin_kb_start)


@bot.message_handler(func=lambda message: message.text == 'Парсер')
def choose_topic(message: Message):
    bot.send_message(message.chat.id, '📰 Введите url')
    bot.register_next_step_handler(message, set_url_parser)


def set_url_parser(message: Message):
    bot.send_message(message.chat.id, get_titles_from_site(message.text.strip()))


@bot.message_handler(func=lambda message: message.text == '📝 Написать статью')
def choose_topic(message: Message):
    bot.send_message(message.chat.id, '📰 Введите название статьи')
    bot.register_next_step_handler(message, set_topic)


def set_topic(message: Message):
    topic = message.text
    bot.send_message(message.chat.id, f'Вы выбрали тему: {topic}', parse_mode='HTML')
    bot.send_message(message.chat.id, '🛎 Статья создаётся 🛎')

    user = CustomUser.objects.get(username='greatarticlesuser')
    article, description, category, title, query_keyword = create_article(topic)

    try:
        category = Category.objects.get(name=category)
    except:
        category = Category.objects.get(name='Образование')

    slug = slugify(title)

    image_url = get_img_from_keyword(query_keyword, title)

    image_filename = image_url.split('/')[-1][:50]

    image_bytes = download_image_from_url(image_url)
    resized_image_bytes = convert_image_to_webp(image_bytes)
    django_file = create_django_file_from_bytes(resized_image_bytes)
    send_article_photo(message, django_file)
    bot.send_message(message.chat.id, '🏞 Выберите изображение')

    bot.register_next_step_handler(
        message, choose_image, title, user, description, article, slug, category, image_filename, django_file,
        query_keyword
    )


def choose_image(
        message: Message, title: str, user: CustomUser, description: str, article: str, slug: str,
        category: Category, image_filename: str, django_file: File, query_keyword: str
):
    if message.text == '❌ Отменить':
        bot.send_message(message.chat.id, '📟 Панель администратора', reply_markup=admin_kb_start)
    elif message.text == '✅ Продолжить':
        create_article_with_image(
            title, user, description, article, slug, category, image_filename, django_file
        )
        bot.send_message(message.chat.id, 'Статья создана')
    elif message.text == '🔄 Пересоздать':
        image_url = get_img_from_keyword(query_keyword, title)
        image_bytes = download_image_from_url(image_url)
        resized_image_bytes = convert_image_to_webp(image_bytes)
        django_file = create_django_file_from_bytes(resized_image_bytes)
        send_article_photo(message, django_file)
        bot.register_next_step_handler(
            message, choose_image, title, user, description, article, slug, category, image_filename, django_file,
            query_keyword
        )


@bot.message_handler(func=lambda message: message.text == '📝 Написать статьи через gpt')
def create_article_with_list(message: Message):
    bot.send_message(message.chat.id, 'Введите количество тем')
    bot.register_next_step_handler(message, generate_article_with_list)


@bot.message_handler(func=lambda message: message.text == '📝 Написать статью через список')
def create_article_with_list(message: Message):
    bot.send_message(message.chat.id, 'Введите список тем через |')
    bot.register_next_step_handler(message, generate_article_with_list)


def generate_article_with_list(message: Message):
    if message.text.isdigit():
        list_titles = create_titles_for_articles(int(message.text)).split('|')
    else:
        list_titles = message.text.split('|')

    user = CustomUser.objects.get(username='greatarticlesuser')

    for n, title in enumerate(list_titles):
        try:
            title = title.strip()
            while True:
                try:
                    article, description, category, title, query_keyword = create_article(title)
                    break  # Выходим из цикла, если выполнение дошло до этой строки
                except APIError:
                    bot.send_message(message.chat.id, f'Статья {n} ошибка')
                    time.sleep(5)
                    continue
            slug = slugify(title)

            try:
                category = Category.objects.get(name=category)
            except:
                category = Category.objects.get(name='Образование')

            image_url = get_img_from_keyword(query_keyword, title)
            image_filename = image_url.split('/')[-1]

            image_bytes = download_image_from_url(image_url)
            resized_image_bytes = convert_image_to_webp(image_bytes)
            django_file = create_django_file_from_bytes(resized_image_bytes)

            create_article_with_image(title, user, description, article, slug, category, image_filename, django_file)
            bot.send_message(message.chat.id, f'Статья {n} создана')
            time.sleep(30)
        except Exception as ex:
            bot.send_message(message.chat.id, f'Ошибка {n} {ex}')
            continue

    bot.send_message(message.chat.id, 'Статьи созданы')
    bot.send_message(message.chat.id, '📟 Панель администратора', reply_markup=admin_kb_start)


class Command(BaseCommand):
    help = 'Create an article through a Telegram bot'

    def handle(self, *args, **options):
        bot.polling()
