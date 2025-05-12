from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import random
from config import TOKEN

# Шутки и анекдоты
jokes = [
    "Почему программисты путают Хэллоуин и Рождество? Потому что OCT 31 == DEC 25.",
    "Гугл: 'Вы имели в виду: помощь программиста'",
    "— Доктор, у меня проблемы с памятью. — С каких пор? — С каких пор что?",
    "Колобок повесился)"
]

# Стартовая команда с кнопками
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("ℹ️ О боте", callback_data="about")],
        [InlineKeyboardButton("📜 Команды", callback_data="help")],
        [InlineKeyboardButton("😂 Анекдот", callback_data="joke")],
        [InlineKeyboardButton("🧠 Решить уравнение", callback_data="math")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Привет! 👋 Я — твой телеграм-бот-помощник.\nВыбери, что хочешь сделать:",
        reply_markup=reply_markup
    )

# Уравнения и ответы
equations = [
    ("2x = 10", "x = 5"),
    ("3x + 6 = 15", "x = 3"),
    ("x/2 = 4", "x = 8"),
]

# Функция для создания inline-кнопок для главного меню
def get_main_keyboard():
    return [
        [
            InlineKeyboardButton("Получить шутку", callback_data='joke'),
            InlineKeyboardButton("Решить уравнение", callback_data='math')
        ],
        [
            InlineKeyboardButton("Информация о боте", callback_data='about')
        ]
    ]

# Функция для создания inline-кнопок для помощи
def get_help_keyboard():
    return [
        [
            InlineKeyboardButton("Команда /start", callback_data='start'),
            InlineKeyboardButton("Команда /help", callback_data='help'),
            InlineKeyboardButton("Команда /about", callback_data='about'),
            InlineKeyboardButton("Команда /joke", callback_data='joke_info'),
            InlineKeyboardButton("Команда /math", callback_data='math_info')
        ]
    ]

# Функция для создания кнопки "Назад"
def get_back_button():
    return [
        [InlineKeyboardButton("Назад", callback_data='back')]
    ]

# Обработчик кнопок
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == 'joke':
        joke = random.choice(jokes)
        keyboard = get_back_button()
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.answer()
        await query.edit_message_text(joke, reply_markup=reply_markup)
    elif query.data == 'math':
        eq, ans = random.choice(equations)
        options = [
            InlineKeyboardButton("x = 4", callback_data=f'answer_{ans}_false'),
            InlineKeyboardButton("x = 5", callback_data=f'answer_{ans}_true'),
            InlineKeyboardButton("x = 6", callback_data=f'answer_{ans}_false'),
            InlineKeyboardButton("x = 7", callback_data=f'answer_{ans}_false')
        ]
        keyboard = InlineKeyboardMarkup([options] + get_back_button())
        await query.answer()
        await query.edit_message_text(f"Реши уравнение: {eq}", reply_markup=keyboard)
    elif query.data == 'answer_x = 5_true':
        await query.answer()
        await query.edit_message_text("Верно! Ответ: x = 5", reply_markup=InlineKeyboardMarkup(get_back_button()))
    elif query.data.startswith('answer_'):
        await query.answer()
        await query.edit_message_text("Неверно. Попробуй еще раз!", reply_markup=InlineKeyboardMarkup(get_back_button()))
    elif query.data == 'start':
        await query.answer()
        keyboard = get_main_keyboard()
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Привет! Я телеграм-бот 😊 Напиши /help чтобы узнать мои команды.", reply_markup=reply_markup)
    elif query.data == 'help':
        await query.answer()
        keyboard = get_help_keyboard()
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "/about - Информация о создателе\n"
            "/help - Список команд\n"
            "/joke - Получить случайную шутку\n"
            "/math - Случайное уравнение с ответом (в спойлере)",
            reply_markup=reply_markup
        )
    elif query.data == 'about':
        await query.answer()
        await query.edit_message_text(
            "Этот бот был создан студентом-программистом 🚀 GitHub: https://github.com/florenway",
            reply_markup=InlineKeyboardMarkup(get_back_button())
        )
    elif query.data == 'joke_info':
        await query.answer()
        await query.edit_message_text(
            "Команда /joke отправляет случайную шутку. Например:\n"
            "\"Почему программисты путают Хэллоуин и Рождество? Потому что OCT 31 == DEC 25.\"",
            reply_markup=InlineKeyboardMarkup(get_back_button())
        )
    elif query.data == 'math_info':
        await query.answer()
        await query.edit_message_text(
            "Команда /math отправляет случайное уравнение с выбором ответа. Например:\n"
            "Реши уравнение: 2x = 10. Ответы: x = 4, x = 5, x = 6, x = 7.",
            reply_markup=InlineKeyboardMarkup(get_back_button())
        )
    elif query.data == 'back':
        await query.answer()
        keyboard = get_main_keyboard()
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Вы в главном меню:", reply_markup=reply_markup)

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = get_main_keyboard()
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Я телеграм-бот 😊 Напиши /help чтобы узнать мои команды.", reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = get_help_keyboard()
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "/about - Информация о создателе\n"
        "/help - Список команд\n"
        "/joke - Получить случайную шутку\n"
        "/math - Случайное уравнение с ответом (в спойлере)",
        reply_markup=reply_markup
    )

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Контакты разработчика", url="https://github.com/florenway")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Этот бот был создан студентом-программистом 🚀", reply_markup=reply_markup)

async def joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    joke = random.choice(jokes)
    keyboard = [
        [InlineKeyboardButton("Еще одну шутку", callback_data="joke")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(joke, reply_markup=reply_markup)

async def math_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    eq, ans = random.choice(equations)
    options = [
        InlineKeyboardButton("x = 4", callback_data=f'answer_{ans}_false'),
        InlineKeyboardButton("x = 5", callback_data=f'answer_{ans}_true'),
        InlineKeyboardButton("x = 6", callback_data=f'answer_{ans}_false'),
        InlineKeyboardButton("x = 7", callback_data=f'answer_{ans}_false')
    ]
    keyboard = InlineKeyboardMarkup([options] + get_back_button())
    await update.message.reply_text(f"Реши уравнение: {eq}", reply_markup=keyboard)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    responses = {
        "привет": "Привет-привет! 👋",
        "как дела": "У меня всё отлично! А у тебя?",
        "что делаешь": "Общаюсь с тобой :)"
    }
    response = responses.get(text, "Я тебя пока не понимаю, но учусь 🧠")
    await update.message.reply_text(response)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("joke", joke_command))
    app.add_handler(CommandHandler("math", math_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(CallbackQueryHandler(button))

    print("Бот запущен...")
    app.run_polling()
