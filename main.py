import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

import google.generativeai as genai
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_message = update.message.text

        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(user_message)

        await update.message.reply_text(response.text)

    except Exception as e:
        await update.message.reply_text("❌ خطا در ارتباط با جمینای.")

app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
app.run_polling()
