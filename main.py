import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

openai.api_key = os.getenv("OPENAI_API_KEY")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_message = update.message.text

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_message}]
        )

        await update.message.reply_text(response.choices[0].message.content)

    except Exception as e:
        await update.message.reply_text(
            "❌ خطا در ارتباط با سرویس. اگر ادامه داشت، یعنی سهمیه تمومه."
        )

app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
app.run_polling()
