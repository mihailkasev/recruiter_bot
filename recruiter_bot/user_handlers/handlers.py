import logging
import os
from datetime import datetime

from telegram import ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler

from db import db
from settings import stream_handler

from . import static_text
from .static_text import age, city, experience, position


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(stream_handler)

QUESTION = range(1)

# устанавливаем ключи для ответов кандидата для записи в бд
QUESTION_KEYS: list = [
    "ФИО", "Город", "Возраст", "Желаемая должность", "Опыт работы"
]

QUESTION_LIST: list = [city, age, position, experience]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начинает разговор с пользователем и спрашивает ФИО."""
    message = update.message
    user = db.get_user(message.chat_id)
    if user["is_passed"]:
        await message.reply_text(
            static_text.cannot_repeat.format(
                user=message.from_user.first_name))
        return ConversationHandler.END

    await message.reply_text(
        static_text.conversation_start)

    logger.info(static_text.logger_start.format(
        user=message.from_user.first_name))

    return QUESTION


async def ask_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Задает вопрос из списка вопросов и переходит к следующему."""
    message = update.message
    user = db.get_user(message.chat_id)
    answer = message.text

    db.set_user(
        message.chat_id,
        {QUESTION_KEYS[user["question_id"]]: answer})

    if user["question_id"] == len(QUESTION_LIST):
        # если вопросы закончились, прекращаем разговор
        await message.reply_text(
            static_text.conversation_end,
            reply_markup=ReplyKeyboardRemove())
        await context.bot.send_message(
            os.getenv("ADMIN_ID"),
            static_text.new_candidate.format(
                user=user["ФИО"]))

        db.set_user(
            message.chat_id,
            {"is_passed": True,
                "created_at": datetime.now().strftime("%d.%m.%y")})

        logger.info(static_text.logger_end.format(
            user=message.from_user.first_name))

        return ConversationHandler.END

    question = QUESTION_LIST[user["question_id"]]
    await message.reply_text(
        question[0],
        reply_markup=question[1]
    )
    db.set_user(
        message.chat_id,
        {"question_id": user["question_id"] + 1}
    )

    return QUESTION


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отменяет разговор и удаляет данные пользователя."""
    user = update.message.from_user
    logger.info(static_text.logger_cancel.format(user=user.first_name))

    await update.message.reply_text(
        static_text.conversation_cancel,
        reply_markup=ReplyKeyboardRemove()
    )
    db.users.delete_one({"chat_id": update.message.chat_id})

    return ConversationHandler.END
