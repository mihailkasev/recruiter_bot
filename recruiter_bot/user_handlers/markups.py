from telegram import ReplyKeyboardMarkup


reply_keyboard_for_position = [
    ["дизайнер", "программист"],
    ["менеджер проекта", "тестировщик"],
    ["системный администратор"]
]
markup_for_position = ReplyKeyboardMarkup(
    reply_keyboard_for_position,
    one_time_keyboard=True
)

reply_keyboard_for_experience = [
    ["Нет", "От 1 до 6 месяцев"],
    ["От 6 до 12 месяцев", "Более 1 года"],
    ["Более 3 лет"],
]
markup_for_experience = ReplyKeyboardMarkup(
    reply_keyboard_for_experience,
    one_time_keyboard=True
)
