import os
from google import genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_message = update.message.text

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=user_message
        )

        await update.message.reply_text(response.text)

    except Exception as e:
        await update.message.reply_text("❌ خطا در ارتباط با جمینای.")

app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
app.run_polling()
