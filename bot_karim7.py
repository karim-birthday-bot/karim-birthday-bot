import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Список подарков
GIFTS = [
    ("Конструктор LEGO Sonic Наклз и главный изумрудный храм, 325 деталей, 76998", "https://ozon.ru/t/8FM5GSK"),
    ("Конструктор LEGO Sonic the Hedgehog Побег ежа Шэдоу, 76995", "https://ozon.ru/t/HO96qWv"),
    ("Конструктор пластиковый", "https://ozon.ru/t/EvHJchU"),
    ("Пижама", "https://ozon.ru/t/AsDmFZE"),
    ("Конструктор LEGO Sonic Мастерская Тейлза и Самолет Торнадо, 376 деталей, 76991", "https://ozon.ru/t/fc8pBHB"),
    ("Подводная маска для плавания Kuchenhaus", "https://ozon.ru/t/4Cf7LuR"),
    ("Эспандер кистевой", "https://ozon.ru/t/7oJYfXm"),
    ("Набор цветных карандашей ГАММА", "https://ozon.ru/t/dhXBGrr")
]

# Словарь для отслеживания выбора подарков
selected_gifts = {}

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    keyboard = [
        [InlineKeyboardButton("Где и когда?", callback_data="location")],
        [InlineKeyboardButton("Что будет?", callback_data="program")],
        [InlineKeyboardButton("Подтвердить участие (RSVP)", callback_data="rsvp")],
        [InlineKeyboardButton("Выбрать подарок", callback_data="gift")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Привет, друг!\n\n"
        "Я — Карим, и 10 июля мне исполняется 7 лет! Добро пожаловать на мой День рождения — здесь ты найдёшь всю самую важную информацию: где мы празднуем, во сколько, что тебя ждёт и как повеселиться на полную!\n\n"
        "Будет весело, ярко и по-настоящему круто! Рад, что ты со мной в этот день!",
        reply_markup=reply_markup
    )

# Обработка кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == "location":
        await query.message.reply_text("Мы собираемся 10 июля в 15:00\nВсеволожск, БО «Топ Лес»\n\nНе опаздывай — будет круто!")

    elif query.data == "program":
        await query.message.reply_text(
            "Тебя ждёт:\n"
            "- Катание на квадроциклах\n"
            "- Лазертаг в лесу\n"
            "- Весёлые танцы с бобром\n"
            "- Торт и подарки\n"
            "- Отличное настроение!"
        )

    elif query.data == "rsvp":
        keyboard = [
            [InlineKeyboardButton("Я точно приду!", callback_data="rsvp_yes")],
            [InlineKeyboardButton("Не получится(", callback_data="rsvp_no")],
            [InlineKeyboardButton("Пока не уверен(а)", callback_data="rsvp_maybe")]
        ]
        await query.message.reply_text("Ты придёшь на праздник?", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith("rsvp_"):
        response = {
            "rsvp_yes": "Спасибо за ответ: «Я точно приду!». До встречи!",
            "rsvp_no": "Жаль, что не получится. Будем скучать!",
            "rsvp_maybe": "Спасибо за ответ! Будем надеяться, что ты сможешь прийти."
        }
        await query.message.reply_text(response.get(query.data, "Спасибо за ответ!"))

    elif query.data == "gift":
        if user_id in selected_gifts:
            await query.message.reply_text("Ты уже выбрал подарок.")
            return

        buttons = []
        for i, (title, url) in enumerate(GIFTS):
            if url not in selected_gifts.values():
                buttons.append([InlineKeyboardButton(f"{i+1}. {title}", callback_data=f"gift_{i}")])

        if not buttons:
            await query.message.reply_text("Все подарки уже выбраны.")
        else:
            await query.message.reply_text("Выбери подарок из списка:", reply_markup=InlineKeyboardMarkup(buttons))

    elif query.data.startswith("gift_"):
        gift_index = int(query.data.split("_")[1])
        gift_title, gift_url = GIFTS[gift_index]
        selected_gifts[user_id] = gift_url
        await query.message.reply_text(
            f"Ты выбрал: {gift_title}\nСсылка: {gift_url}\n\nСпасибо! Подарок помечен как выбранный."
        )

# Основной запуск бота
if __name__ == '__main__':
    TOKEN = os.getenv("TOKEN")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()