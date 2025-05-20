from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    PollHandler,
    ContextTypes,
)
import logging

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Главное меню
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Где и когда?", callback_data='place')],
        [InlineKeyboardButton("Что будет?", callback_data='program')],
        [InlineKeyboardButton("Подтвердить участие (RSVP)", callback_data='rsvp')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Привет, друг!\n\n"
        "Я — Карим, и 10 июля мне исполняется 7 лет!\n"
        "Добро пожаловать на мой День рождения — здесь ты найдёшь всю самую важную информацию: "
        "где мы празднуем, во сколько, что тебя ждёт и как повеселиться на полную!\n\n"
        "Будет весело, ярко и по-настоящему круто!\n"
        "Рад, что ты со мной в этот день!",
        reply_markup=reply_markup
    )

# Обработка кнопок
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'program':
        await query.edit_message_text(
            "Ты готов к самому весёлому дню лета?\n\n"
            "Тебя ждёт:\n"
            "- Лазертаг в лесу — как в настоящем боевике!\n"
            "- Катание на квадроциклах — рев мотора, ветер в лицо и драйв!\n"
            "- Весёлые танцы с настоящим бобром!\n"
            "- Огромный торт и сюрпризы!\n\n"
            "Будет шумно, ярко и очень весело!\n"
            "Такое точно нельзя пропустить!"
        )
    elif query.data == 'place':
        await query.edit_message_text(
            "Мы собираемся:\n\n"
            "10 июля в 15:00\n"
            "Всеволожск, БО «Топ Лес»\n\n"
            "Не забудь взять хорошее настроение!"
        )
    elif query.data == 'rsvp':
        await query.message.reply_poll(
            question="Ты придёшь на мой День рождения?",
            options=["Да, конечно!", "Нет, не получится", "Подумаю"],
            is_anonymous=False,
            allows_multiple_answers=False
        )

# Обработка ответа на опрос
async def handle_poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.poll_answer.user
    answer = update.poll_answer.option_ids[0]
    options = ["Да", "Нет", "Подумаю"]

    response = f"{user.full_name} выбрал вариант: {options[answer]}"
    logging.info(response)

    # Отправим ответ родителям (например, админу)
    ADMIN_CHAT_ID = 123456789  # ЗАМЕНИ на свой Telegram ID
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=response)

# Запуск бота
app = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()  # ЗАМЕНИ на свой токен

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_callback))
app.add_handler(PollHandler(handle_poll_answer))

app.run_polling()