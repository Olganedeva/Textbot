from telegram import Update
from telegram.ext import ContextTypes
from keyboards import (
get_main_keyboard,
get_preview_keyboard,
get_confirm_publish_keyboard,
get_schedule_keyboard,
get_confirm_schedule_keyboard,
get_posts_keyboard
)

from datetime import datetime,timedelta
import sqlite3
import logging
from ai import process_text
from tts import text_to_speech

conn=sqlite3.connect("posts.db",check_same_thread=False)
c=conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS posts(
id INTEGER PRIMARY KEY AUTOINCREMENT,
text TEXT,
scheduled_time TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS channels(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
channel_id INTEGER
)
""")

conn.commit()


# ---------------- START ----------------

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
    "Главное меню",
    reply_markup=get_main_keyboard()
    )


async def help_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    text="""
/start запуск
/menu меню
/connect_channel подключить канал
"""
    await update.message.reply_text(text)


# ---------------- ПОДКЛЮЧЕНИЕ КАНАЛА ----------------

async def connect_channel(update:Update,context:ContextTypes.DEFAULT_TYPE):
    context.user_data["waiting_channel"]=True
    await update.message.reply_text(
    "Перешлите сообщение из канала.\nБот должен быть администратором."
    )


# ---------------- ОБРАБОТКА СООБЩЕНИЙ ----------------

async def handle_message(update:Update,context:ContextTypes.DEFAULT_TYPE):

    text=update.message.text


    # редактирование времени
    if context.user_data.get("edit_post_id"):
        post_id=context.user_data.pop("edit_post_id")
        try:
            new_time=datetime.strptime(text,"%d.%m.%Y %H:%M")

            c.execute(
            "UPDATE posts SET scheduled_time=? WHERE id=?",
            (new_time.strftime("%Y-%m-%d %H:%M"),post_id)
            )

            conn.commit()

            await update.message.reply_text(
            "Время поста обновлено",
            reply_markup=get_main_keyboard()
            )

        except:
            await update.message.reply_text("Формат: ДД.ММ.ГГГГ ЧЧ:ММ")
            context.user_data["edit_post_id"]=post_id
        return


    # подключение канала
    if context.user_data.get("waiting_channel"):

        context.user_data["waiting_channel"]=False

        if update.message.forward_origin:

            try:

                channel=update.message.forward_origin.chat
                channel_id=channel.id
                user_id=update.message.from_user.id

                c.execute(
                "INSERT INTO channels(user_id,channel_id) VALUES(?,?)",
                (user_id,channel_id)
                )

                conn.commit()

                await update.message.reply_text(
                f"Канал подключён\nID:{channel_id}"
                )

            except:
                await update.message.reply_text(
                "Не удалось определить канал."
                )

        else:
            await update.message.reply_text(
            "Перешлите сообщение из канала."
            )

        return


    # ввод текста поста
    if context.user_data.get("waiting_post"):

        context.user_data["waiting_post"]=False
        context.user_data["post_text"]=text

        await update.message.reply_text(
        f"Предпросмотр:\n\n{text}",
        reply_markup=get_preview_keyboard()
        )

        return


    # ввод времени
    if context.user_data.get("waiting_time"):

        try:

            t=datetime.strptime(text,"%d.%m.%Y %H:%M")

            context.user_data["scheduled_time"]=t
            context.user_data["waiting_time"]=False

            post=context.user_data.get("post_text")

            await update.message.reply_text(
            f"{post}\n\nПубликация:{t.strftime('%d.%m.%Y %H:%M')}",
            reply_markup=get_confirm_schedule_keyboard()
            )

        except:
            await update.message.reply_text(
            "Формат: ДД.ММ.ГГГГ ЧЧ:ММ"
            )

        return


    await update.message.reply_text(
    "Используйте меню",

    reply_markup=get_main_keyboard()
    )
    if context.user_data.get("process_text"):
        context.user_data["process_text"] = False
        result = process_text(update.message.text)
        context.user_data["post_text"] = result
        await update.message.reply_text(
            f"✏️ Обработанный текст:\n\n{result}",
            reply_markup=get_preview_keyboard()
        )
        return


# ---------------- CALLBACK ----------------

async def button_callback(update:Update,context:ContextTypes.DEFAULT_TYPE):

    query=update.callback_query
    await query.answer()

    data=query.data


    if data=="main_menu":

        context.user_data.clear()

        await query.message.edit_text(
        "Главное меню",
        reply_markup=get_main_keyboard()
        )

        return


    if data=="upload_post":

        context.user_data["waiting_post"]=True

        await query.message.edit_text(
        "Отправьте текст поста"
        )

        return


    if data=="publish_post":

        post=context.user_data.get("post_text")

        await query.message.edit_text(
        f"Опубликовать пост?\n\n{post}",
        reply_markup=get_confirm_publish_keyboard()
        )

        return


    if data=="confirm_publish_yes":

        await query.message.edit_text(
        "Выберите время",
        reply_markup=get_schedule_keyboard()
        )

        return


    if data=="confirm_publish_no":

        context.user_data.clear()

        await query.message.edit_text(
        "Публикация отменена",
        reply_markup=get_main_keyboard()
        )

        return


    # выбор времени
    if data.startswith("schedule_"):

        if data=="schedule_now":
            t=datetime.now()

        elif data=="schedule_1m":
            t=datetime.now()+timedelta(minutes=1)

        elif data=="schedule_2m":
            t=datetime.now()+timedelta(minutes=2)

        elif data=="schedule_custom":

            context.user_data["waiting_time"]=True

            await query.message.edit_text(
            "Введите дату\nДД.ММ.ГГГГ ЧЧ:ММ"
            )

            return


        context.user_data["scheduled_time"]=t
        post=context.user_data.get("post_text")

        await query.message.edit_text(
        f"{post}\n\nПубликация:{t.strftime('%d.%m.%Y %H:%M')}",
        reply_markup=get_confirm_schedule_keyboard()
        )

        return


    # подтверждение
    if data=="confirm_schedule_yes":

        post=context.user_data.get("post_text")
        t=context.user_data.get("scheduled_time")

        delay=(t-datetime.now()).total_seconds()
        if delay<0:delay=0

        c.execute(
        "INSERT INTO posts(text,scheduled_time) VALUES(?,?)",
        (post,t.strftime("%Y-%m-%d %H:%M"))
        )

        conn.commit()

        context.job_queue.run_once(
        publish_post_job,
        delay,
        chat_id=query.message.chat_id,
        data=post
        )

        context.user_data.clear()

        await query.message.edit_text(
        "Пост запланирован",
        reply_markup=get_main_keyboard()
        )

        return


    # график
    if data=="schedule_view":

        c.execute("SELECT id,text,scheduled_time FROM posts ORDER BY scheduled_time")
        posts=c.fetchall()

        if not posts:

            await query.message.edit_text(
            "Нет запланированных постов",
            reply_markup=get_main_keyboard()
            )

            return


        text="📅 Запланированные посты\n\n"

        for p in posts:
            preview=p[1][:30].replace("\n"," ")
            text+=f"{p[2]} — {preview}...\n"

        await query.message.edit_text(
        text,
        reply_markup=get_posts_keyboard(posts)
        )

        return


    if data.startswith("delete_"):

        post_id=int(data.split("_")[1])

        c.execute("DELETE FROM posts WHERE id=?",(post_id,))
        conn.commit()

        await query.message.edit_text(
        "Пост удалён",
        reply_markup=get_main_keyboard()
        )

        return


    if data.startswith("edit_"):

        post_id=int(data.split("_")[1])

        context.user_data["edit_post_id"]=post_id

        await query.message.edit_text(
        "Введите новое время\nДД.ММ.ГГГГ ЧЧ:ММ"
        )

        return

    if data == "voice_post":
        text = context.user_data.get("post_text")
        if not text:
            await query.message.edit_text("Нет текста для озвучки")
            return
        file_path = text_to_speech(text)
        if file_path:
            await context.bot.send_voice(
                chat_id=query.message.chat_id,
                voice=open(file_path, "rb")
            )
        else:
            await query.message.edit_text("Ошибка озвучки")

        return


# ---------------- ПУБЛИКАЦИЯ ----------------

async def publish_post_job(context:ContextTypes.DEFAULT_TYPE):

    job=context.job
    user_id=job.chat_id

    c.execute(
    "SELECT channel_id FROM channels WHERE user_id=? ORDER BY id DESC LIMIT 1",
    (user_id,)
    )

    result=c.fetchone()

    if not result:
        logging.error("Канал не подключён")
        return

    channel_id=result[0]

    try:

        await context.bot.send_message(
        chat_id=channel_id,
        text=job.data
        )

    except Exception as e:
        logging.error(f"Ошибка публикации:{e}")


# ---------------- ВОССТАНОВЛЕНИЕ ПОСТОВ ----------------

def load_scheduled_posts(app):

    c.execute("SELECT text,scheduled_time FROM posts")

    posts=c.fetchall()

    for p in posts:

        text=p[0]
        t=datetime.strptime(p[1],"%Y-%m-%d %H:%M")

        delay=(t-datetime.now()).total_seconds()

        if delay<0:
            continue

        app.job_queue.run_once(
        publish_post_job,
        delay,
        data=text
        )