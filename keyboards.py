from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta

def get_main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Загрузить пост", callback_data="upload_post")],
        [InlineKeyboardButton("🔊 Озвучить", callback_data="voice_post")],
        [InlineKeyboardButton("⏱ Отложка", callback_data="schedule")],
        [InlineKeyboardButton("📅 График", callback_data="schedule_view")]
    ])

def get_preview_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔊 Озвучить", callback_data="voice_post")],
        [InlineKeyboardButton("Опубликовать", callback_data="publish_post")],
        [InlineKeyboardButton("Редактировать", callback_data="edit_post_copy")],
        [InlineKeyboardButton("Меню", callback_data="main_menu")]
    ])

def get_confirm_publish_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Да", callback_data="confirm_publish_yes"),
         InlineKeyboardButton("Нет", callback_data="confirm_publish_no")]
    ])

def get_schedule_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Сейчас", callback_data="schedule_now")],
        [InlineKeyboardButton("+1 мин", callback_data="schedule_1m")],
        [InlineKeyboardButton("+2 мин", callback_data="schedule_2m")],
        [InlineKeyboardButton("Ввести", callback_data="schedule_custom")]
    ])

def get_confirm_schedule_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Подтвердить", callback_data="confirm_schedule_yes")],
        [InlineKeyboardButton("Изменить", callback_data="confirm_schedule_edit")],
        [InlineKeyboardButton("Меню", callback_data="main_menu")]
    ])


# -------- КАЛЕНДАРЬ --------

def get_calendar_keyboard():
    buttons = []
    today = datetime.now().date()
    for i in range(7):
        d = today + timedelta(days=i)
        buttons.append([InlineKeyboardButton(
            d.strftime("%d.%m"),
            callback_data=f"day_{d.strftime('%Y-%m-%d')}"
        )])
    buttons.append([InlineKeyboardButton("Меню", callback_data="main_menu")])
    return InlineKeyboardMarkup(buttons)


def get_hours_keyboard(date):
    buttons = []
    for h in range(24):
        buttons.append([InlineKeyboardButton(
            f"{h:02}:00",
            callback_data=f"hour_{date}_{h}"
        )])
    buttons.append([InlineKeyboardButton("Назад", callback_data="schedule_view")])
    return InlineKeyboardMarkup(buttons)


def get_posts_in_hour_keyboard(posts):
    buttons=[]
    for p in posts:
        buttons.append([InlineKeyboardButton(
            f"{p[2][-5:]} | {p[1][:10]}",
            callback_data=f"post_{p[0]}"
        )])
    buttons.append([InlineKeyboardButton("Назад", callback_data="calendar_back")])
    return InlineKeyboardMarkup(buttons)