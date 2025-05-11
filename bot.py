from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import random
from config import TOKEN

# Шутки и анекдоты
jokes = [
    "Почему программисты путают Хэллоуин и Рождество? Потому что OCT 31 == DEC 25.",
    "Гугл: 'Вы имели в виду: помощь программиста'",
    "— Доктор, у меня проблемы с памятью. — С каких пор? — С каких пор что?"
]

# Уравнения
equations = [
    ("2x = 10", "x = 5"),
    ("3x + 6 = 15", "x = 3"),
    ("x/2 = 4", "x = 8"),
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я телеграм-бот 😊 Напиши /help чтобы узнать мои команды.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/about - Информация о создателе\n"
        "/help - Список команд\n"
        "/joke - Получить случайную шутку\n"
        "/math - Случайное уравнение с ответом (в спойлере)"
    )

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Этот бот был создан студентом-программистом 🚀 GitHub: https://github.com/florenway")

async def joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    joke = random.choice(jokes)
    await update.message.reply_text(joke)

async def math_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    eq, ans = random.choice(equations)
    await update.message.reply_text(f"Реши уравнение: {eq}\nОтвет: ||{ans}||")

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

    print("Бот запущен...")
    app.run_polling()
