import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Включаем логгирование
logging.basicConfig(level=logging.INFO)

# Приветственное сообщение
WELCOME_TEXT = (
    "Привет, друг!\n\n"
    "Я — Карим, и 10 июля мне исполняется 7 лет!\n"
    "Добро пожаловать на мой День рождения — здесь ты найдёшь всю самую важную информацию:\n"
    "где мы празднуем, во сколько, что тебя ждёт и как повеселиться на полную!\n\n"
    "Будет весело, ярко и по-настоящему круто!\n"
    "Рад, что ты со мной в этот день!"
)

# Обработка команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Где и когда?", callback_data="info_place")],
        [InlineKeyboardButton("Что будет?", callback_data="info_program")],
        [InlineKeyboardButton("Подтвердить участие (RSVP)", callback_data="info_rsvp")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(WELCOME_TEXT, reply_markup=reply_markup)

# Обработка кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "info_place":
        await query.edit_message_text("Мы ждём тебя **10 июля в 15:00** по адресу: \n_Санкт-Петербург, ул. Весёлая, 7 (детский центр FunCity)_.")
    elif query.data == "info_program":
        await query.edit_message_text("Тебя ждёт:\n- Весёлый квест\n- Аниматоры\n- Тортик и подарки\n- Играем до 18:00!")
    elif query.data == "info_rsvp":
        await query.edit_message_text("Напиши моим родителям, если ты точно придёшь:\n@mama_karima или @papa_karima")

# Запуск бота
if __name__ == '__main__':
    import os
    from dotenv import load_dotenv
    load_dotenv()

    TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()