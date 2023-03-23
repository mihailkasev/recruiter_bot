import logging
from telegram import Update
from telegram.ext import CallbackContext, ContextTypes

from db import db
from settings import file_storage, stream_handler

from .static_text import (file_not_found, logger_message, message_command,
                          message_success, message_no_text,
                          message_wrong_command, message_wrong_fio)
from .utils import check_permission, write_candidate_to_file


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(stream_handler)


async def export_users(update: Update, context: CallbackContext) -> None:
    """Формирует текстовый файл с данными пользователей и отправляет админу."""
    message = update.message
    user = await db.get_user(message.chat_id)
    if not await check_permission(user, update):
        return

    users = db.users.find(
        {"is_passed": True, "is_exported": False, "is_admin": False},
        {
            "_id": 0, "is_exported": 0, "is_admin": 0,
            "is_passed": 0, "question_id": 0
        }
    )
    async for user in users:
        chat_id = write_candidate_to_file(user)
        await db.set_user(chat_id, {"is_exported": True})

    try:
        file = open(file_storage, "rb")
    except FileNotFoundError:
        logger.warning(file_not_found)
        await message.reply_text(
            file_not_found
        )
        return
    await message.reply_document(file)


async def send_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Отправляет сообщение выбранному кандидату."""
    message = update.message
    user = await db.get_user(message.chat_id)
    if not await check_permission(user, update):
        return

    if message.text == message_command:
        await update.message.reply_text(
            message_wrong_command.format(
                command=message_command
            )
        )
        return

    text = f"{message.text.replace(f'{message_command} ', '')}"
    text_list = text.split(",")
    if text_list[1] == "":
        await update.message.reply_text(
            message_no_text
        )
        return
    candidate = await db.users.find_one({"ФИО": text_list[0]}, {"chat_id": 1})
    if candidate is None:
        await update.message.reply_text(
            message_wrong_fio
        )
        return
    await context.bot.send_message(
        chat_id=candidate['chat_id'],
        text=text.split(" ", 1)[1],  # возьмем только имя и отчество
    )
    logger.info(logger_message.format(user=text_list[0]))
    await update.message.reply_text(
        message_success
    )
