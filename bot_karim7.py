from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters
import os

TOKEN = os.getenv("TOKEN")

rsvp_options = ["Я точно приду!", "Не получится(", "Пока не уверен(а)"]

wishlist = [
    ("LEGO Sonic Храм, 325 деталей", "https://ozon.ru/t/8FM5GSK"),
    ("LEGO Sonic Побег ежа Шэдоу", "https://ozon.ru/t/HO96qWv"),
    ("Пластиковый конструктор", "https://ozon.ru/t/EvHJchU"),
    ("Пижама", "https://ozon.ru/t/AsDmFZE"),
    ("LEGO Sonic Мастерская Тейлза", "https://ozon.ru/t/fc8pBHB"),
    ("Маска для плавания L/XL", "https://ozon.ru/t/4Cf7LuR"),
    ("Эспандер для рук", "https://ozon.ru/t/7oJYfXm"),
    ("Карандаши ГАММА", "https://ozon.ru/t/dhXBGrn"),
]

selected_gifts = set()


def main_menu():
    keyboard = [
        [InlineKeyboardButton("Где и когда?", callback_data="place")],
        [InlineKeyboardButton("Что будет?", callback_data="details")],
        [InlineKeyboardButton("Подтвердить участие (RSVP)", callback_data="rsvp")],
        [InlineKeyboardButton("Выбрать подарок", callback_data="wishlist")],
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Привет, друг!\n\n"
        "Я — Карим, и 10 июля мне исполняется 7 лет!\n"
        "Добро пожаловать на мой День рождения — здесь ты найдёшь всю самую важную информацию:\n"
        "где мы празднуем, во сколько, что тебя ждёт и как повеселиться на полную!\n\n"
        "Будет весело, ярко и по-настоящему круто!\nРад, что ты со мной в этот день!"
    )
    await update.message.reply_text(text, reply_markup=main_menu())


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "place":
        await query.edit_message_text("Мы собираемся 10 июля в 16:00\nВсеволожск, БО «Топ Лес»\nНе опаздывай — будет круто!", reply_markup=main_menu())

    elif query.data == "details":
        await query.edit_message_text("Тебя ждёт праздник с играми, подарками, вкусной едой и волшебной атмосферой. Приходи в хорошем настроении!", reply_markup=main_menu())

    elif query.data == "rsvp":
        buttons = [[InlineKeyboardButton(text, callback_data=f"rsvp_{i}")] for i, text in enumerate(rsvp_options)]
        await query.edit_message_text("Подтверди, пожалуйста, своё участие:\nТы придёшь на праздник?", reply_markup=InlineKeyboardMarkup(buttons))

    elif query.data.startswith("rsvp_"):
        index = int(query.data.split("_")[1])
        answer = rsvp_options[index]
        await query.edit_message_text(f"Спасибо за ответ: «{answer}».\nДо встречи!")

    elif query.data == "wishlist":
        buttons = []
        for i, (title, link) in enumerate(wishlist):
            if i not in selected_gifts:
                buttons.append([InlineKeyboardButton(f"{title}", callback_data=f"gift_{i}")])
            else:
                buttons.append([InlineKeyboardButton(f"❌ {title}", callback_data="taken")])
        buttons.append([InlineKeyboardButton("Назад в меню", callback_data="back_to_menu")])
        await query.edit_message_text("Выбери подарок, который хочешь подарить:", reply_markup=InlineKeyboardMarkup(buttons))

    elif query.data.startswith("gift_"):
        gift_id = int(query.data.split("_")[1])
        if gift_id in selected_gifts:
            await query.answer("Этот подарок уже выбрали!", show_alert=True)
            return
        selected_gifts.add(gift_id)
        title, link = wishlist[gift_id]
        await query.edit_message_text(f"Спасибо! Ты выбрал подарок: {title}\nСсылка: {link}")

    elif query.data == "taken":
        await query.answer("Этот подарок уже выбран.", show_alert=True)

    elif query.data == "back_to_menu":
        await query.edit_message_text("Главное меню:", reply_markup=main_menu())


if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()