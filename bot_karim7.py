from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = "7884639351:AAHekyYrrQjdRNBmT1Nt1PjoRNLjLxGbz78"

# Приветствие
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Где и когда?", callback_data="place_time")],
        [InlineKeyboardButton("Что будет?", callback_data="program")],
        [InlineKeyboardButton("Подтвердить участие (RSVP)", callback_data="rsvp")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message = (
        "Привет, друг!\n\n"
        "Я — Карим, и 10 июля мне исполняется 7 лет!\n"
        "Добро пожаловать на мой День рождения — здесь ты найдёшь всю самую важную информацию:\n"
        "где мы празднуем, во сколько, что тебя ждёт и как повеселиться на полную!\n\n"
        "Будет весело, ярко и по-настоящему круто!\n"
        "Рад, что ты со мной в этот день!"
    )

    await update.message.reply_text(message, reply_markup=reply_markup)

# Ответы на кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "place_time":
        await query.edit_message_text(
            "Ждём тебя **10 июля в 15:00** по адресу: *Всеволожск, БО 'Топ Лес'*"
        )
    elif query.data == "program":
        await query.edit_message_text(
            "Тебя ждёт:\n"
            "- Катание на квадроциклах\n"
            "- Лазертаг в лесу\n"
            "- Весёлые танцы с Бобром\n"
            "- Торт, угощения и сюрпризы!"
        )
    elif query.data == "rsvp":
        keyboard = [
            [InlineKeyboardButton("Я приду!", callback_data="yes")],
            [InlineKeyboardButton("К сожалению, нет", callback_data="no")]
        ]
        await query.edit_message_text("Ты придёшь на праздник?", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data == "yes":
        await query.edit_message_text("Ура! До встречи на празднике!")
    elif query.data == "no":
        await query.edit_message_text("Жаль, что не получится. Надеюсь увидеться в другой раз!")

# Запуск
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()