from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)
import json
import os

# === ЗАМЕНИ НА СВОЙ ТОКЕН ===
TOKEN = "7884639351:AAHekyYrrQjdRNBmT1NtlPjoRNLjLxGbz78"

# === Список подарков ===
GIFTS = [
    "Лего", "Книга про динозавров", "Набор для рисования",
    "Соник-фигурка", "Пазл 3D", "Подарочный сертификат"
]

WISHLIST_FILE = "wishlist.json"
RSVP_FILE = "rsvp.json"

# === Чтение / сохранение JSON-файлов ===
def load_data(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# === /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Где и когда?", callback_data="place")],
        [InlineKeyboardButton("Что будет?", callback_data="program")],
        [InlineKeyboardButton("Подтвердить участие (RSVP)", callback_data="rsvp")],
        [InlineKeyboardButton("Выбрать подарок (вишлист)", callback_data="wishlist")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "Привет, друг!\n\n"
        "Я — Карим, и 10 июля мне исполняется 7 лет!\n"
        "Добро пожаловать на мой День рождения — здесь ты найдёшь всю самую важную информацию:\n"
        "где мы празднуем, во сколько, что тебя ждёт и как повеселиться на полную!\n\n"
        "Будет весело, ярко и по-настоящему круто!\n"
        "Рад, что ты со мной в этот день!"
    )
    await update.message

