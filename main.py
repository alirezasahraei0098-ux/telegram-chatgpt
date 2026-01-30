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

        # استخراج امن متن
        if response.candidates and len(response.candidates) > 0:
            parts = response.candidates[0].content.parts
            if parts and len(parts) > 0:
                text = parts[0].text
            else:
                text = "❌ جمینای پاسخی نداد."
        else:
            text = "❌ جمینای پاسخی نداد."

        await update.message.reply_text(text)

    except Exception as e:
        # این خط خیلی مهمه: خطای واقعی رو تو لاگ می‌نویسه
        print("GEMINI ERROR:", e)
        await update.message.reply_text("❌ خطا در پردازش پاسخ جمینای.")

app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
import os

PORT = int(os.environ.get("PORT", 8080))
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    url_path="webhook",
    webhook_url=f"{WEBHOOK_URL}/webhook"
)

