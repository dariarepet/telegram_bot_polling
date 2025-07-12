import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

buttons = [
    ["🧾 Обо мне", "🎯 Абонементы"],
    ["📚 Курс для репетиторов", "✨ Пробное занятие"]
]
keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

ABOUT_LINK = "https://daria-emelianova.yonote.ru/share/rus"
ABONEMENT_LINK = "https://daria-emelianova.yonote.ru/share/abonement"
KURS_LINK = "https://daria-emelianova.yonote.ru/share/kabinet"
PROBNOE_LINK = "https://forms.yandex.ru/u/683ad41feb61464bc78c1b3e"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я бот Дарьи Емельяновой. Чем могу помочь?",
        reply_markup=keyboard
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    if text == "🧾 Обо мне":
        await update.message.reply_text(f"Вот информация обо мне:\n{ABOUT_LINK}")
    elif text == "🎯 Абонементы":
        await update.message.reply_text(f"Все тарифы и абонементы тут:\n{ABONEMENT_LINK}")
    elif text == "📚 Курс для репетиторов":
        await update.message.reply_text(f"Курс находится тут:\n{KURS_LINK}")
    elif text == "✨ Пробное занятие":
        await update.message.reply_text(f"Заполните форму на пробное занятие:\n{PROBNOE_LINK}")
    else:
        username = user.username or user.first_name or "пользователь"
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"📩 Вопрос от @{username} (id {user.id}):\n{text}"
        )
        await update.message.reply_text("Ваш вопрос отправлен. Я скоро отвечу ✨")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()