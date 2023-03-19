import os

from telegram.ext import (Application, CommandHandler, ConversationHandler,
                          MessageHandler, filters)
from dotenv import load_dotenv

from error import send_error_message
from admin_handlers.handlers import export_users, send_message
from admin_handlers.static_text import message_command
from user_handlers.handlers import QUESTION, ask_question, cancel, start


load_dotenv()

recruiter_bot = Application.builder().token(
    os.getenv("TELEGRAM_TOKEN")).build()

recruiter_bot.add_handler(
    ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            QUESTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND,
                               ask_question),
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
)
recruiter_bot.add_handler(
    CommandHandler("export_users", export_users)
)
recruiter_bot.add_handler(
    MessageHandler(filters.Regex(rf'^{message_command}(/s)?.*'), send_message)
)
recruiter_bot.add_error_handler(send_error_message)
