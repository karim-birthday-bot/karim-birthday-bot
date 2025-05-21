import logging from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes import os

TOKEN = os.getenv("TOKEN")

Список подарков

GIFTS = { "gift1": ("Конструктор LEGO Sonic Наклз и главный изумрудный храм, 325 деталей, 76998", "https://ozon.ru/t/BFM5GSK"), "gift2": ("Конструктор LEGO Sonic the Hedgehog Побег ежа Шэдоу, 76995", "https://ozon.ru/t/HO96qWv"), "gift3": ("Конструктор пластиковый", "https://ozon.ru/t/EvHJchU"), "gift4": ("Пижама", "https://ozon.ru/t/AsDmFZE"), "gift5": ("Конструктор LEGO Sonic Мастерская Тейлза и Самолет Торнадо, 376 деталей, 6+, 76991", "https://ozon.ru/t/fc8pBHB"), "gift6": ("Подводная маска для плавания Kuchenhaus", "https://ozon.ru/t/4Cf7LuR"), "gift7": ("Эспандер кистевой для рук 3в1", "https://ozon.ru/t/7oJYfXm"), "gift8": ("Набор двусторонних цветных карандашей ГАММА", "https://ozon.ru/t/dhXBGrn") } selected_gifts = set()

Главное меню

main_menu = ReplyKeyboardMarkup( keyboard=[ ["Где и когда?", "Что будет?"], ["Подтвердить участие (RSVP)", "Выбрать подарок"] ], resize_keyboard=True )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: await update.message.reply_text( "Привет, друг!\n\n" "Я — Карим, и 10 июля мне исполняется 7 лет!\n" "Добро пожаловать на мой День рождения — здесь ты найдёшь всю самую важную информацию: где мы празднуем, во сколько, что тебя ждёт и как повеселиться на полную!\n\n" "Будет весело, ярко и по-настоящему круто!\nРад, что ты со мной в этот день!", reply_markup=main_menu )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: text = update.message.text if text == "Где и когда?": await update.message.reply_text( "Мы собираемся 10 июля в 16:00 в \nВсеволожск, БО "Топ Лес"\n\nНе опаздывай — будет круто!" ) elif text == "Что будет?": await update.message.reply_text( "Тебя ждёт настоящее приключение:\n— батут\n— квест\n— много вкусной еды\n— торт\n— и подарки!" ) elif text == "Подтвердить участие (RSVP)": keyboard = [ [InlineKeyboardButton("Я точно приду!", callback_data="yes")], [InlineKeyboardButton("Не получится(", callback_data="no")], [InlineKeyboardButton("Пока не уверен(а)", callback_data="maybe")] ] await update.message.reply_text("Подтверди, пожалуйста, своё участие:\nТы придёшь на праздник?", reply_markup=InlineKeyboardMarkup(keyboard)) elif text == "Выбрать подарок": keyboard = [] for key, (title, link) in GIFTS.items(): if key not in selected_gifts: keyboard.append([InlineKeyboardButton(title[:30] + "...", callback_data=key)]) if keyboard: await update.message.reply_text("Выбери один из подарков:", reply_markup=InlineKeyboardMarkup(keyboard)) else: await update.message.reply_text("Все подарки уже выбраны другими гостями.")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: query = update.callback_query await query.answer() data = query.data

if data in ["yes", "no", "maybe"]:
    answers = {
        "yes": "Спасибо за ответ: «Я точно приду!». До встречи!",
        "no": "Жаль, что не получится. Надеюсь увидеться в другой раз!",
        "maybe": "Хорошо, дай знать, когда решишься!"
    }
    await query.edit_message_text(answers[data])
elif data in GIFTS:
    if data in selected_gifts:
        await query.edit_message_text("Этот подарок уже выбран. Пожалуйста, выбери другой.")
    else:
        selected_gifts.add(data)
        title, link = GIFTS[data]
        await query.edit_message_text(f"Спасибо! Ты выбрал подарок: {title}\n\nСсылка на него: {link}")

if name == 'main': logging.basicConfig(level=logging.INFO) app = Application.builder().token(TOKEN).build() app.add_handler(CommandHandler("start", start)) app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)) app.add_handler(CallbackQueryHandler(handle_callback)) app.run_polling()

