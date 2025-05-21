from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters import os

TOKEN = os.getenv("TOKEN")

Список подарков с названиями и ссылками

GIFTS = [ ("LEGO Sonic: Храм и Наклз", "https://ozon.ru/t/BFM5GSK"), ("LEGO Sonic: Побег Шэдоу", "https://ozon.ru/t/HO96qWv"), ("Конструктор пластиковый", "https://ozon.ru/t/EvHJchU"), ("Пижама", "https://ozon.ru/t/AsDmFZE"), ("LEGO Sonic: Мастерская и Самолёт", "https://ozon.ru/t/fc8pBHB"), ("Маска для плавания Kuchenhaus", "https://ozon.ru/t/4Cf7LuR"), ("Эспандер 3в1, бирюзовый", "https://ozon.ru/t/7oJYfXm"), ("Карандаши ГАММА 12 шт.", "https://ozon.ru/t/dhXBGrn"), ]

selected_gifts = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): keyboard = [[InlineKeyboardButton(gift[0], callback_data=f"gift_{i}")] for i, gift in enumerate(GIFTS) if i not in selected_gifts] reply_markup = InlineKeyboardMarkup(keyboard) await update.message.reply_text("Выбери подарок из списка (после выбора он будет скрыт):", reply_markup=reply_markup)

async def gift_choice(update: Update, context: ContextTypes.DEFAULT_TYPE): query = update.callback_query await query.answer() gift_index = int(query.data.split('_')[1]) selected_gifts.add(gift_index) name, link = GIFTS[gift_index] await query.edit_message_text(text=f"Ты выбрал подарок: {name}\nСсылка: {link}")

application = Application.builder().token(TOKEN).build()

application.add_handler(CommandHandler("start", start)) application.add_handler(CallbackQueryHandler(gift_choice, pattern=r"^gift_\d+$"))

application.run_polling()

