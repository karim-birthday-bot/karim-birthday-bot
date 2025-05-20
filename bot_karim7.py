import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Загружаем переменные из .env (если ты тестируешь локально)
load_dotenv()

# Получаем токен из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")

# Функция, которая обрабатывает команду /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Добро пожаловать на день рождения Карима!\n"
        "Здесь ты найдёшь всю информацию о празднике!"
    )

# Запуск приложения
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()