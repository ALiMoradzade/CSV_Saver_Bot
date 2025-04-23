from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from typing import Final
import os
import csv_handler
import date_time

# Install python-telegram-bot

# bot initial
load_dotenv()
TELEGRAM_BOT_TOKEN: Final = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_BOT_USERNAME: Final = os.getenv("TELEGRAM_BOT_USERNAME")
ADMIN_USERNAME: Final = os.getenv("ADMIN_USERNAME")
LOG_PATH: Final = "log.txt"


def write_log_command(user_id: str, command: str):
    with open(LOG_PATH, 'a') as file:
        file.write(f'{date_time.tehran_datetime("%Y/%m/%d, %H:%M")} - @{user_id} => \"/{command}\"\n')


def write_log_text(text: str, end: str = '\n'):
    with open(LOG_PATH, 'a', encoding='utf-8') as file:
        file.write(text + end)


def clear_log_file():
    open(LOG_PATH, 'w').close()


def successful_message():
    text = "✅ با موفقیت انجام شده!"
    return text


def access_denied_message():
    text = "❌ دسترسی بسته شد!"
    return text


# Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    write_log_command(update.message.chat.username, 'start')
    await update.message.reply_text("سلام خوش امدید")
    await update.message.reply_text("لطفا مقادیر زیر را وارد کنید...\nنام تامین کننده\nنام محصول\nقیمت روز\nشرایط پرداخت")


async def send_csv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    write_log_command(update.message.chat.username, 'send_csv')
    await update.message.reply_text('در حال ارسال⬆️...')
    await update.message.reply_document(csv_handler.path)


async def clear_csv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    write_log_command(update.message.chat.username, 'clear_csv')
    if update.message.chat.username == ADMIN_USERNAME:
        await update.message.reply_text('🫡الساعه...')
        csv_handler.clear()
        await update.message.reply_text(successful_message())
    else:
        await update.message.reply_text(access_denied_message())


async def send_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    write_log_command(update.message.chat.username, 'send_log')
    if update.message.chat.username == ADMIN_USERNAME:
        await update.message.reply_text('در حال ارسال⬆️...')
        await update.message.reply_document(LOG_PATH)
    else:
        await update.message.reply_text(access_denied_message())


async def clear_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    write_log_command(update.message.chat.username, 'clear_log')
    if update.message.chat.username == ADMIN_USERNAME:
        await update.message.reply_text('🫡الساعه...')
        clear_log_file()
        await update.message.reply_text(successful_message())
    else:
        await update.message.reply_text(access_denied_message())


# Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if "hello" in processed or "hi" in processed:
        return "Hello, welcome"
    elif "سلام" in processed:
        return "سلام خوش آمدید"
    else:
        return "در دستور کار نیست"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    write_log_text(f'{date_time.tehran_datetime("%Y/%m/%d, %H:%M")} - ({message_type}) @{update.message.chat.username} => \"{text.replace('\n', '\\n')}\"')

    text_splited = text.splitlines()

    if len(text_splited) == 4:
        csv_handler.append(text_splited, False)
        await update.message.reply_text(successful_message())
    else:
        await update.message.reply_text(handle_response(text))


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    write_log_text(f'{date_time.tehran_datetime("%Y/%m/%d, %H:%M")} - Update => {update}, caused error => {context.error}')


# Robot
if __name__ == '__main__':
    print('Starting...')

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('send_csv', send_csv))
    app.add_handler(CommandHandler('clear_csv', clear_csv))
    app.add_handler(CommandHandler('send_log', send_log))
    app.add_handler(CommandHandler('clear_log', clear_log))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Error
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)
