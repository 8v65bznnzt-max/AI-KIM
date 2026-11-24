import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ContextTypes, filters
)

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("Не задан токен Telegram-бота.")

MENU = ReplyKeyboardMarkup(
    [["👋 Привет", "👋 Пока"], ["ℹ️ Помощь"]],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я AI Kim 🤖\n"
        "Пока я учусь. Скоро подключим настоящий ИИ!",
        reply_markup=MENU
    )

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Чем займёмся?",
        reply_markup=MENU
    )

async def bye(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Пока! До скорой встречи 👋")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start — открыть меню\n"
        "/hello — поздороваться\n"
        "/bye — попрощаться\n"
        "/help — помощь",
        reply_markup=MENU
    )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip().lower()

    if text in ("привет", "здравствуй", "здравствуйте", "👋 привет"):
        await hello(update, context)
    elif text in ("пока", "до свидания", "👋 пока"):
        await bye(update, context)
    elif text in ("помощь", "ℹ️ помощь"):
        await help_command(update, context)
    else:
        await update.message.reply_text(
            "Я пока учусь отвечать. Скоро подключим ИИ!",
            reply_markup=MENU
        )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("bye", bye))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
