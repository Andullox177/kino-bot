from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "7356647239:AAE2bRh9KIyeGiPA3WgOWjXZbhQt5fP7y8Y"

movies = {
    "K100": "https://archive.org/details/night_of_the_living_dead",
    "K101": "https://archive.org/details/charlie_chaplin-the-kid"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Kino kodini yuboring\nMasalan: K100"
    )

async def get_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.upper()

    if code in movies:
        await update.message.reply_text(f"🎥 Kino:\n{movies[code]}")
    else:
        await update.message.reply_text("❌ Bunday kod topilmadi")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_movie))

app.run_polling()
