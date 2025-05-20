
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging

API_TOKEN = '7884639351:AAHekyYrrQjdRNBmT1NtlPjoRNLjLxGbz78'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

reserved_gifts = set()

gifts = [
    {
        "id": "gift1",
        "title": "LEGO Sonic: Наклз и главный изумрудный храм (76998)",
        "link": "https://ozon.ru/t/BFM5GSK"
    },
    {
        "id": "gift2",
        "title": "LEGO Sonic: Побег ежа Шэдоу (76995)",
        "link": "https://ozon.ru/t/HO96qWv"
    },
    {
        "id": "gift3",
        "title": "Конструктор пластиковый",
        "link": "https://ozon.ru/t/EvHJchU"
    },
    {
        "id": "gift4",
        "title": "Пижама",
        "link": "https://ozon.ru/t/AsDmFZE"
    },
    {
        "id": "gift5",
        "title": "LEGO Sonic: Мастерская Тейлза и самолёт Торнадо (76991)",
        "link": "https://ozon.ru/t/fc8pBHB"
    },
    {
        "id": "gift6",
        "title": "Подводная маска Kuchenhaus (L/XL, чёрная)",
        "link": "https://ozon.ru/t/4Cf7LuR"
    },
]

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("✅ Я приду", callback_data="rsvp_yes"),
        InlineKeyboardButton("❌ Не смогу", callback_data="rsvp_no"),
        InlineKeyboardButton("🎁 Посмотреть вишлист", callback_data="view_wishlist")
    )
    await message.answer(
        "Привет! Ты приглашён на день рождения Карима!

"
        "Ему исполняется 7 лет!
"
        "Празднуем 10 июля в 15:00
"
        "Место: Всеволожск, БО «Топ Лес»

"
        "Будет весело! Приходи!",
        reply_markup=kb
    )

@dp.callback_query_handler(lambda c: c.data)
async def process_callback(callback_query: types.CallbackQuery):
    data = callback_query.data

    if data == "rsvp_yes":
        await callback_query.message.answer("Класс! Жду тебя!")
    elif data == "rsvp_no":
        await callback_query.message.answer("Жаль, что не получится. Будем на связи!")
    elif data == "view_wishlist":
        for gift in gifts:
            if gift["id"] not in reserved_gifts:
                reserve_btn = InlineKeyboardMarkup().add(
                    InlineKeyboardButton("Забронировать", callback_data=f"reserve_{gift['id']}")
                )
                await callback_query.message.answer(f"{gift['title']}
{gift['link']}", reply_markup=reserve_btn)
    elif data.startswith("reserve_"):
        gift_id = data.replace("reserve_", "")
        reserved_gifts.add(gift_id)
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer("Спасибо! Этот подарок теперь забронирован. Сюрприз сохранён!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
