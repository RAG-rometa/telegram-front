import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Save your token in a .env file
RAG_API_URL = os.getenv("RAG_API_URL")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text("🔍 Searching...")

    try:
        response = requests.post(RAG_API_URL, json={"question": query})
        data = response.json()

        if response.status_code == 200:
            await update.message.reply_text(data["answer"])
        else:
            await update.message.reply_text(f"❌ Error: {data.get('error', 'Unknown error')}")

    except Exception as e:
        await update.message.reply_text(f"❌ Request failed: {str(e)}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
