from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from keyboards import *
from datetime import datetime,timedelta
import sqlite3, logging
from ai import process_text
from tts import text_to_speech

conn=sqlite3.connect("posts.db",check_same_thread=False)
c=conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS posts(id INTEGER PRIMARY KEY AUTOINCREMENT,text TEXT,scheduled_time TEXT)")
c.execute(
    "CREATE TABLE IF NOT EXISTS channels(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,channel_id INTEGER)")
conn.commit()


# ---------- START ----------
async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Главное меню", reply_markup=get_main_keyboard())

async def help_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start /menu /connect_channel")


# ---------- CHANNEL ----------
async def connect_channel(update:Update,context:ContextTypes.DEFAULT_TYPE):
    context.user_data["waiting_channel"]=True
    await update.message.reply_text("Перешли сообщение из канала")


# ---------- MESSAGE ----------
async def handle_message(update:Update,context:ContextTypes.DEFAULT_TYPE):
    text=update.message.text

    if context.user_data.get("waiting_channel"):
        context.user_data["waiting_channel"]=False
        if update.message.forward_origin:
            try:
                ch = update.message.forward_origin.chat
                c.execute("INSERT INTO channels(user_id,channel_id) VALUES(?,?)", (update.message.from_user.id, ch.id))
                conn.commit()
                await update.message.reply_text(f"Канал подключён: {ch.id}")
            except:
                await update.message.reply_text("Ошибка")
        else:
            await update.message.reply_text("Нужно переслать сообщение")
        return

    if context.user_data.get("waiting_post"):
        context.user_data["waiting_post"]=False
        try:
            processed = process_text(text)
        except:
            processed = text
        context.user_data["post_text"] = processed
        await update.message.reply_text(processed, reply_markup=get_preview_keyboard())
        return

    if context.user_data.get("waiting_time"):
        try:
            t=datetime.strptime(text,"%d.%m.%Y %H:%M")
            context.user_data["scheduled_time"]=t
            context.user_data["waiting_time"]=False
            post=context.user_data.get("post_text")
            await update.message.reply_text(
                f"{post}\n\n{t.strftime('%d.%m.%Y %H:%M')}",
                reply_markup=get_confirm_schedule_keyboard())
        except:
            await update.message.reply_text("Формат ДД.ММ.ГГГГ ЧЧ:ММ")
        return

    if context.user_data.get("edit_post_id"):
        pid = context.user_data.pop("edit_post_id")
        try:
            t = datetime.strptime(text, "%d.%m.%Y %H:%M")
            c.execute("UPDATE posts SET scheduled_time=? WHERE id=?", (t.strftime("%Y-%m-%d %H:%M"), pid))
            conn.commit()
            await update.message.reply_text("Обновлено", reply_markup=get_main_keyboard())
        except:
            context.user_data["edit_post_id"] = pid
            await update.message.reply_text("Формат неверный")
        return

    await update.message.reply_text("Используй меню", reply_markup=get_main_keyboard())


# ---------- CALLBACK ----------
async def button_callback(update:Update,context:ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    d = q.data

    if d == "main_menu":
        context.user_data.clear()
        await q.message.edit_text("Меню", reply_markup=get_main_keyboard())
        return

    if d == "upload_post":
        context.user_data["waiting_post"]=True
        await q.message.edit_text("Отправь текст")
        return

    if d == "edit_post_copy":
        context.user_data["waiting_post"] = True
        await q.message.edit_text("Новый текст")
        return

    if d == "publish_post":
        post=context.user_data.get("post_text")
        if not post:
            await q.message.edit_text("Нет текста")
            return
        await q.message.edit_text(post + "\n\nОпубликовать?", reply_markup=get_confirm_publish_keyboard())
        return

    if d == "confirm_publish_no":
        context.user_data.clear()
        await q.message.edit_text("Отменено", reply_markup=get_main_keyboard())
        return

    if d == "confirm_publish_yes":
        await q.message.edit_text("Выбери время", reply_markup=get_schedule_keyboard())
        return

    if d == "schedule":
        if not context.user_data.get("post_text"):
            await q.message.edit_text("Сначала загрузи пост")
            return
        await q.message.edit_text("Выбери время", reply_markup=get_schedule_keyboard())
        return

    if d in ["schedule_now", "schedule_1m", "schedule_2m", "schedule_custom"]:
        if d == "schedule_now":
            t = datetime.now()
        elif d == "schedule_1m":
            t = datetime.now() + timedelta(minutes=1)
        elif d == "schedule_2m":
            t = datetime.now() + timedelta(minutes=2)
        else:
            context.user_data["waiting_time"]=True
            await q.message.edit_text("Введите дату")
            return

        context.user_data["scheduled_time"]=t
        post=context.user_data.get("post_text")
        await q.message.edit_text(
            f"{post}\n\n{t.strftime('%d.%m.%Y %H:%M')}",
            reply_markup=get_confirm_schedule_keyboard())
        return

    if d == "confirm_schedule_edit":
        context.user_data["waiting_time"] = True
        await q.message.edit_text("Введите новую дату")
        return

    if d == "confirm_schedule_yes":
        post=context.user_data.get("post_text")
        t=context.user_data.get("scheduled_time")
        if not post or not t:
            await q.message.edit_text("Ошибка данных")
            return

        delay = max((t - datetime.now()).total_seconds(), 0)

        c.execute("INSERT INTO posts(text,scheduled_time) VALUES(?,?)", (post, t.strftime("%Y-%m-%d %H:%M")))
        conn.commit()

        context.job_queue.run_once(publish_post_job, delay, chat_id=q.message.chat_id, data=post)

        context.user_data.clear()
        await q.message.edit_text("Запланировано", reply_markup=get_main_keyboard())
        return

    # ---------- КАЛЕНДАРЬ ----------
    if d == "schedule_view":
        await q.message.edit_text("Выбери день", reply_markup=get_calendar_keyboard())
        return

    if d.startswith("day_"):
        date = d.split("_")[1]
        await q.message.edit_text("Выбери час", reply_markup=get_hours_keyboard(date))
        return

    if d.startswith("hour_"):
        _, date, h = d.split("_")
        start = f"{date} {int(h):02}:00"
        end = f"{date} {int(h):02}:59"

        c.execute("SELECT id,text,scheduled_time FROM posts WHERE scheduled_time BETWEEN ? AND ?", (start, end))
        posts=c.fetchall()

        if not posts:
            await q.message.edit_text("Нет постов", reply_markup=get_calendar_keyboard())
            return

        await q.message.edit_text("Посты", reply_markup=get_posts_in_hour_keyboard(posts))
        return

    if d.startswith("post_"):
        pid = int(d.split("_")[1])
        c.execute("SELECT text,scheduled_time FROM posts WHERE id=?", (pid,))
        p = c.fetchone()

        if not p:
            await q.message.edit_text("Не найден")
            return

        await q.message.edit_text(
            f"{p[1]}\n\n{p[0]}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Редактировать", callback_data=f"edit_{pid}")],
                [InlineKeyboardButton("Удалить", callback_data=f"delete_{pid}")],
                [InlineKeyboardButton("Назад", callback_data="schedule_view")]
            ]))
        return

    if d == "calendar_back":
        await q.message.edit_text("Выбери день", reply_markup=get_calendar_keyboard())
        return

    if d.startswith("delete_"):
        pid = int(d.split("_")[1])
        c.execute("DELETE FROM posts WHERE id=?", (pid,))
        conn.commit()
        await q.message.edit_text("Удалено", reply_markup=get_main_keyboard())
        return

    if d.startswith("edit_"):
        context.user_data["edit_post_id"] = int(d.split("_")[1])
        await q.message.edit_text("Введите новую дату")
        return

    if d == "voice_post":
        text = context.user_data.get("post_text")
        if not text:
            await q.message.edit_text("Нет текста")
            return
        file = text_to_speech(text)
        if file:
            await context.bot.send_voice(chat_id=q.message.chat_id, voice=open(file, "rb"))
        else:
            await q.message.edit_text("Ошибка озвучки")
        return


# ---------- ПУБЛИКАЦИЯ ----------
async def publish_post_job(context:ContextTypes.DEFAULT_TYPE):
    job=context.job
    c.execute("SELECT channel_id FROM channels WHERE user_id=? ORDER BY id DESC LIMIT 1", (job.chat_id,))
    r = c.fetchone()
    if not r: return
    try:
        await context.bot.send_message(chat_id=r[0], text=job.data)
    except Exception as e:
        logging.error(e)


# ---------- ВОССТАНОВЛЕНИЕ ----------
def load_scheduled_posts(app):
    c.execute("SELECT text,scheduled_time FROM posts")
    for text, t in c.fetchall():
        t = datetime.strptime(t, "%Y-%m-%d %H:%M")
        delay=(t-datetime.now()).total_seconds()
        if delay > 0:
            app.job_queue.run_once(publish_post_job, delay, data=text)
