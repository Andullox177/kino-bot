import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, ContextTypes, filters
)

# ====== RENDER UCHUN WEB SERVER ======
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_web():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

threading.Thread(target=run_web, daemon=True).start()
# ====================================

BOT_TOKEN = os.environ.get("7356647239:AAECWUz3o2VKBq0QZ0lfHQZiVynIxZMSSbU")  # Render Environment Variable
ADMIN_ID = 6531073126                     # O'zingizning Telegram ID
CHANNEL = "@kino_uz_channel"              # faqat @username

movies = {}  # code: file_id

async def check_sub(user_id, bot):
    member = await bot.get_chat_member(CHANNEL, user_id)
    return member.status not in ["left", "kicked"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Kino kodini yuboring")

async def set_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    try:
        code = context.args[0].upper()
        context.user_data["code"] = code
        await update.message.reply_text(f"🎯 Endi videoni yuboring ({code})")
    except:
        await update.message.reply_text("Misol: /code K123")

async def save_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not context.user_data.get("code"):
        await update.message.reply_text("❌ Avval /code K123 yozing")
        return
    code = context.user_data["code"]
    movies[code] = update.message.video.file_id
    context.user_data["code"] = None
    await update.message.reply_text(f"✅ Kino saqlandi: {code}")

async def get_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.upper()
    if code not in movies:
        await update.message.reply_text("❌ Bunday kod yo‘q")
        return
    if not await check_sub(update.effective_user.id, context.bot):
        await update.message.reply_text(f"❗ Avval {CHANNEL} kanaliga obuna bo‘ling")
        return
    await update.message.reply_video(movies[code])

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("code", set_code))
app.add_handler(MessageHandler(filters.VIDEO, save_movie))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_movie))
app.run_polling()
