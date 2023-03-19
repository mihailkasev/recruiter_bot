from telegram import Update
from settings import file_storage

from .static_text import first_line, only_for_admin


async def check_permission(user, update: Update) -> bool:
    """Проверяет права доступа."""
    if not user["is_admin"]:
        await update.message.reply_text(only_for_admin)
        return False
    return True


def write_candidate_to_file(user: dict) -> int:
    """Записывает данные кандидата в отдельный doc файл для удобства."""
    with open(file_storage, "a") as file:
        chat_id = user.pop("chat_id")
        fio = user.pop("ФИО")
        date = user.pop("created_at")
        file.write(first_line.format(user=fio, date=date))
        for key, value in user.items():
            file.write(f"{key}: {value}.\n")
        file.write("\n")
    return chat_id
