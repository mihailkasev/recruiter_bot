import html
import os
import logging
import traceback

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from admin_handlers.static_text import (
    error_message_for_admin, error_message_for_user, error)

from db import db
from settings import file_handler, stream_handler


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)


async def send_error_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Отлавливает ошибки обновления
    и направляет сообщения пользователю и админу."""
    logger.error(error, exc_info=context.error)

    user = db.get_user(update.message.chat_id)

    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    message = error_message_for_admin.format(string=html.escape(tb_string))
    await context.bot.send_message(
        chat_id=user["chat_id"],
        text=error_message_for_user
    )
    await context.bot.send_message(
        chat_id=os.getenv("ADMIN_ID"),
        text=message,
        parse_mode=ParseMode.HTML
    )
