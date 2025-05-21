import logging
import os
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Подарки
GIFTS = [
    ("Конструктор LEGO Sonic Наклз и главный изумрудный храм", "https://ozon.ru/t/BFM5GSK"),
    ("Конструктор LEGO Sonic Побег ежа Шэдоу", "https://ozon.ru/t/HO96qWv"),
    ("Конструктор пластиковый", "https://ozon.ru/t/EvHJchU"),
    ("Пижама", "https://ozon.ru/t/AsDmFZE"),
    ("Конструктор LEGO Мастерская Тейлза и Самолет", "https://ozon.ru/t/fc8pBHB"),
    ("Маска для плавания Kuchenhaus", "https://ozon.ru/t/4Cf7LuR"),
    ("Эспандер кистевой", "https://ozon.ru/t/7oJYfXm"),
    ("Карандаши ГАММА", "https://ozon.ru/t/dhXBGrn"),
]

# Словарь для отслеживания выбора подарков
selected_gifts = {}

# Приветствие
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    selected_gifts[user_id] = None
    welcome_text = (
        "Привет, друг!\n\n"
        "Я — Карим, и 10 июля мне исполняется 7 лет!\n"
        "Добро пожаловать на мой День рождения — здесь ты найдёшь всю самую важную информацию: "
        "где мы празднуем, во сколько, что тебя ждёт и как повеселиться на полную!\n\n"
        "Будет весело, ярко и по-настоящему круто! Рад, что ты со мной в этот день!"
    )

    menu_keyboard = [["Где и когда?", "Что будет?"],
                     ["Подтвердить участие (RSVP)", "Выбрать подарок"]]

    await update.message.reply_text(
        welcome_text,
        reply_markup=ReplyKeyboardMarkup(menu_keyboard, resize_keyboard=True)
    )

# Информация о месте
async def where(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Мы собираемся 10 июля в 15:00, Всеволожск, БО «Топ Лес»\n\nНе опаздывай — будет круто!")

# Информация о программе
async def what(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Тебя ждёт:\n"
        "- Катание на квадроциклах\n"
        "- Лазертаг в лесу\n"
        "- Весёлые танцы с бобром\n"
        "- Торт и подарки\n"
        "- Отличное настроение!"
    )

# RSVP
async def rsvp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Я точно приду!", callback_data="rsvp_yes"),
            InlineKeyboardButton("Не получится(", callback_data="rsvp_no"),
            InlineKeyboardButton("Пока не уверен(а)", callback_data="rsvp_maybe"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Подтверди, пожалуйста, своё участие:\nТы придёшь на праздник?", reply_markup=reply_markup)

# Обработка RSVP кнопок
async def rsvp_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    response_map = {
        "rsvp_yes": "Спасибо за ответ: «Я точно приду!». До встречи!",
        "rsvp_no": "Спасибо за ответ: «Не получится(». Будем скучать!",
        "rsvp_maybe": "Спасибо за ответ: «Пока не уверен(а)». Сообщи нам позже!",
    }
    await query.edit_message_text(text=response_map.get(query.data, "Спасибо за ответ!"))

# Выбор подарка
async def choose_gift(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if selected_gifts.get(user_id):
        await update.message.reply_text("Ты уже выбрал подарок.")
        return

    buttons = [
        [InlineKeyboardButton(text=title, url=url, callback_data=f"gift_{i}")]
        for i, (title, url) in enumerate(GIFTS)
    ]
    await update.message.reply_text("Выбери подарок по ссылке и нажми кнопку, чтобы его закрепить.", reply_markup=InlineKeyboardMarkup(buttons))

# Обработка выбора подарка
async def handle_gift_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if selected_gifts.get(user_id):
        await query.answer("Ты уже выбрал подарок.")
        return

    index = int(query.data.split("_")[1])
    selected_gifts[user_id] = index
    await query.answer()
    await query.edit_message_text(text=f"Спасибо! Ты выбрал: {GIFTS[index][0]}.")

# Обработка текстовых кнопок
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Где и когда?":
        await where(update, context)
    elif text == "Что будет?":
        await what(update, context)
    elif text == "Подтвердить участие (RSVP)":
        await rsvp(update, context)
    elif text == "Выбрать подарок":
        await choose_gift(update, context)

# Запуск бота
if __name__ == '__main__':
    import asyncio
    from telegram.ext import defaults

    TOKEN = os.getenv("TOKEN")
    if not TOKEN:
        raise RuntimeError("Переменная окружения TOKEN не установлена.")

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(rsvp_response, pattern="^rsvp_"))
    application.add_handler(CallbackQueryHandler(handle_gift_selection, pattern="^gift_"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    application.run_polling()