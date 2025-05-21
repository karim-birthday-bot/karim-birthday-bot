from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from datetime import datetime
import os

TOKEN = os.getenv("TOKEN")

rsvp_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("Я точно приду!", callback_data="yes")],
    [InlineKeyboardButton("Не получится(", callback_data="no")],
    [InlineKeyboardButton("Пока не уверен(а)", callback_data="maybe")]
])

main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Где и когда?"), KeyboardButton("Что будет?")],
        [KeyboardButton("Подтвердить участие (RSVP)")]
    ],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_text = (
        "Привет, друг!\n\n"
        "Я — Карим, и 10 июля мне исполняется 7 лет!\n"
        "Добро пожаловать на мой День рождения — здесь ты найдёшь всю самую важную информацию: "
        "где мы празднуем, во сколько, что тебя ждёт и как повеселиться на полную!\n\n"
        "Будет весело, ярко и по-настоящему круто!\n"
        "Рад, что ты со мной в этот день!"
    )
    await update.message.reply_text(start_text, reply_markup=main_menu_keyboard)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Где и когда?":
        await update.message.reply_text("Мы собираемся 10 июля в 16:00\nВсеволожск, БО «Топ Лес»\n\nНе опаздывай — будет круто!")
    elif text == "Что будет?":
        await update.message.reply_text("Будет весёлый праздник с играми, угощениями, тортом и сюрпризами!")
    elif text == "Подтвердить участие (RSVP)":
        await update.message.reply_text("Подтверди, пожалуйста, своё участие:\nТы придёшь на праздник?", reply_markup=rsvp_keyboard)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    response_map = {
        "yes": "Спасибо за ответ: «Я точно приду!». До встречи!",
        "no": "Жаль, что не получится. Но мы будем на связи!",
        "maybe": "Хорошо, напомню ближе к дате. Спасибо!"
    }

    response = response_map.get(query.data, "Ответ получен.")
    await query.edit_message_text(response)

    # После ответа возвращаем основное меню
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text="Чем ещё могу помочь?",
        reply_markup=main_menu_keyboard
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()