from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta


# Главное меню
def get_main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Загрузить пост", callback_data="upload_post")],
        [InlineKeyboardButton("🔊 Озвучить", callback_data="voice_post")],
        [InlineKeyboardButton("⏱ Отложка", callback_data="schedule")],
        [InlineKeyboardButton("📅 График", callback_data="schedule_view")]
    ])


# Предпросмотр поста
def get_preview_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔊 Озвучить", callback_data="voice_post")],
        [InlineKeyboardButton("Опубликовать", callback_data="publish_post")],
        [InlineKeyboardButton("Редактировать текст", callback_data="edit_post_copy")],
        [InlineKeyboardButton("Главное меню", callback_data="main_menu")]
    ])


# Подтверждение публикации
def get_confirm_publish_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Да", callback_data="confirm_publish_yes"),
         InlineKeyboardButton("Нет", callback_data="confirm_publish_no")]
    ])


# Подтверждение отмены публикации
def get_confirm_cancel_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Да", callback_data="confirm_cancel_yes"),
         InlineKeyboardButton("Нет", callback_data="confirm_cancel_no")]
    ])


# Кнопки для действий с запланированными постами
def get_post_actions_keyboard(posts):
    buttons = []
    for post in posts:
        buttons.append([
            InlineKeyboardButton(f"Изменить {post[2]}", callback_data=f"edit_time_{post[0]}"),
            InlineKeyboardButton(f"Удалить {post[2]}", callback_data=f"delete_post_{post[0]}")
        ])
    return InlineKeyboardMarkup(buttons)


# Выбор времени для отложенной публикации
def get_schedule_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Отложить на сейчас", callback_data="schedule_now")],
        [InlineKeyboardButton("Отложить на 1 минуту", callback_data="schedule_1m")],
        [InlineKeyboardButton("Отложить на 2 минуты", callback_data="schedule_2m")],
        [InlineKeyboardButton("Выбрать время", callback_data="schedule_custom")]
    ])


# Подтверждение отложенной публикации
def get_confirm_schedule_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Подтвердить", callback_data="confirm_schedule_yes")],
        [InlineKeyboardButton("Изменить время", callback_data="confirm_schedule_edit")],
        [InlineKeyboardButton("Главное меню", callback_data="main_menu")]
    ])

def get_posts_keyboard(posts):
    buttons=[]
    for p in posts:
        buttons.append([
            InlineKeyboardButton(f"✏ Редактировать {p[2]}",callback_data=f"edit_{p[0]}"),
            InlineKeyboardButton("❌ Отмена",callback_data=f"delete_{p[0]}")
        ])
    buttons.append([InlineKeyboardButton("⬅ Меню",callback_data="main_menu")])
    return InlineKeyboardMarkup(buttons)