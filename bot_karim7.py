import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

gifts = [
    {"name": "LEGO Sonic: Наклз и изумрудный храм", "url": "https://ozon.ru/t/8FM5GSK"},
    {"name": "LEGO Sonic: Побег ежа Шэдоу", "url": "https://ozon.ru/t/HO96qWv"},
    {"name": "Пластиковый конструктор", "url": "https://ozon.ru/t/EvHJchU"},
    {"name": "Пижама", "url": "https://ozon.ru/t/AsDmFZE"},
    {"name": "LEGO Sonic: Самолёт Торнадо", "url": "https://ozon.ru/t/fc8pBHB"},
    {"name": "Маска для плавания", "url": "https://ozon.ru/t/4Cf7LuR"},
    {"name": "Эспандер для рук", "url": "https://ozon.ru/t/7oJYfXm"},
    {"name": "Цветные карандаши", "url": "https://ozon.ru/t/dhXBGrn"},
]

chosen_gifts = {}

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        ["Где и когда?", "Что будет?"],
        ["Подтвердить участие (RSVP)", "Выбрать подарок"]
    ],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет, друг!\n\n"
        "Я — Карим, и 10 июля мне исполняется 7 лет!\n"
        "Добро пожаловать на мой День рождения — здесь ты найдёшь всю самую важную информацию: "
        "где мы празднуем, во сколько, что тебя ждёт и как повеселиться на полную!\n\n"
        "Будет весело, ярко и по-настоящему круто!\n"
        "Рад, что ты со мной в этот день!",
        reply_markup=main_menu
    )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Где и когда?":
        await update.message.reply_text("Мы собираемся 10 июля в 16:00, Всеволожск, БО «Топ Лес».")
    elif text == "Что будет?":
        await update.message.reply_text("Будет аниматор, квест, подарки, бассейн и пицца!")
    elif text == "Подтвердить участие (RSVP)":
        keyboard = [
            [InlineKeyboardButton("Я точно приду!", callback_data="RSVP_1")],
            [InlineKeyboardButton("Не получится(", callback_data="RSVP_2")],
            [InlineKeyboardButton("Пока не уверен(а)", callback_data="RSVP_3")]
        ]
        await update.message.reply_text(
            "Подтверди, пожалуйста, своё участие:\nТы придёшь на праздник?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif text == "Выбрать подарок":
        keyboard = []
        for i, gift in enumerate(gifts):
            if i not in chosen_gifts.values():
                keyboard.append([InlineKeyboardButton(gift["name"], callback_data=f"gift_{i}")])
        if not keyboard:
            await update.message.reply_text("Все подарки уже выбраны.")
        else:
            await update.message.reply_text("Выбери подарок из списка:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("RSVP_"):
        options = {
            "RSVP_1": "«Я точно приду!»",
            "RSVP_2": "«Не получится(»",
            "RSVP_3": "«Пока не уверен(а)»"
        }
        await query.edit_message_text(f"Спасибо за ответ: {options[query.data]}. До встречи!")
    elif query.data.startswith("gift_"):
        gift_id = int(query.data.split("_")[1])
        user_id = query.from_user.id

        if user_id in chosen_gifts:
            await query.edit_message_text("Ты уже выбрал подарок.")
            return

        chosen_gifts[user_id] = gift_id
        gift = gifts[gift_id]

        await query.edit_message_text("Спасибо! Ссылка на подарок отправлена в личные сообщения.")
        await context.bot.send_message(chat_id=user_id, text=f"Ты выбрал: {gift['name']}\n{gift['url']}")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.run_polling()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()