from telebot.types import (
    ReplyKeyboardMarkup, KeyboardButton,
)

admin_kb_choose_topic = ['❌ Отменить', '✅ Продолжить', '🔄 Пересоздать']


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(*items)
    return keyboard


admin_kb_start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
admin_kb_start.add(KeyboardButton(text='📝 Написать статью'), KeyboardButton(text='📝 Написать статью через список'), KeyboardButton(text='Парсер'), KeyboardButton(text='📝 Написать статьи через gpt'))
