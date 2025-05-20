from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from datetime import datetime

TOKEN = "7884639351:AAHekyYrrQjdRNBmT1NtlPjoRNLjLxGbz78"
ADMIN_CHAT_ID = 805971875  # Твой Telegram ID (куда приходят уведомления)

# Приветствие
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Где и когда?", callback_data='place')],
        [InlineKeyboardButton("Что будет?", callback_data='program')],
        [InlineKeyboardButton("Подтвердить участие (RSVP)", callback_data='rsvp')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "Привет, друг!\n\n"
        "Я — Карим, и 10 июля мне исполняется 7 лет!\n"
        "Добро пожаловать на мой День рождения — здесь ты найдёшь всю самую важную информацию:\n"
        "где мы празднуем, во сколько, что тебя ждёт и как повеселиться на полную!\n\n"
        "Будет весело, ярко и по-настоящему круто!\n"
        "Рад, что ты со мной в этот день!"
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# Обработка кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'place':
        await query.edit_message_text(
            "Мы собираемся 10 июля в 15:00\n"
            "Всеволожск, БО «Топ Лес»\n\n"
            "Не опаздывай — будет круто!"
        )

    elif query.data == 'program':
        await query.edit_message_text(
            "Тебя ждёт:\n"
            "- Катание на квадроциклах\n"
            "- Лазертаг в лесу\n"
            "- Весёлые танцы с бобром\n"
            "- Торт и подарки\n"
            "- Отличное настроение!"
        )

    elif query.data == 'rsvp':
        keyboard = [
            ["Я точно приду!"],
            ["Не получится("],
            ["Пока не уверен(а)"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await query.edit_message_text("Подтверди, пожалуйста, своё участие:")
        await query.message.reply_text("Ты придёшь на праздник?", reply_markup=reply_markup)

# Обработка ответа RSVP
async def rsvp_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    text = update.message.text
    time = datetime.now().strftime("%d.%m %H:%M")

    # Ответ пользователю
    await update.message.reply_text(f"Спасибо за ответ: «{text}». До встречи!")

    # Уведомление тебе (организатору)
    name = user.full_name
    username = f"@{user.username}" if user.username else "(без username)"
    notify = f"**{name}** ({username}) выбрал: _{text}_\n({time})"
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=notify, parse_mode="Markdown")

# Запуск
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, rsvp_reply))
    app.run_polling()

if __name__ == "__main__":
    main()