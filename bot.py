import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters)
from telegram.request import HTTPXRequest
from telegram import BotCommand
from config import TOKEN
from handlers import start, handle_message, button_callback, connect_channel, help_command,load_scheduled_posts
import sqlite3

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


async def set_commands(app):
    commands = [
        BotCommand("start", "Запустить бота"),
        BotCommand("connect_channel", "Подключить канал для публикации"),
        BotCommand("help", "Показать помощь"),
        BotCommand("menu", "Открыть главное меню")
    ]

    await app.bot.set_my_commands(commands)

def main():
    request = HTTPXRequest(
        connection_pool_size=50,
        pool_timeout=60.0,
        connect_timeout=30.0,
        read_timeout=30.0,
        write_timeout=30.0,
    )

    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .request(request)
        .build()
    )

    app.post_init = set_commands


    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("connect_channel", connect_channel))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_callback))

    conn = sqlite3.connect("posts.db")

    conn.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY,
        text TEXT,
        scheduled_time TEXT,
        channel_id INTEGER,
        status TEXT
    )
    """)

    conn.commit()

    app.bot_data["db_conn"] = conn

    print("Бот запущен...")
    load_scheduled_posts(app)
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
