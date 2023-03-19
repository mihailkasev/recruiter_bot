from .markups import markup_for_position, markup_for_experience

conversation_start = """
Добрый день! Рады Вас здесь видеть.
Мы хотим с Вами познакомиться поближе и по итогу договориться о собеседовании.
Напишите свою фамилию, имя, отчество.
"""

# перечень вопросов, который так же можно дополнить ["вопрос", клавиатура]
city = ["В каком городе Вы живете?", None]
age = ["Сколько Вам лет?", None]
position = ["На какую должность Вы рассчитываете?", markup_for_position]
experience = ["Какой опыт работы Вы имеете?", markup_for_experience]

conversation_cancel = "Разговор отменен."
conversation_end = "Спасибо за данные ответы! Мы с Вами свяжемся!"
cannot_repeat = """
{user}, Ваша кандидатура уже находится на рассмотрении. Мы с Вами свяжемся.
"""
new_candidate = "Получены данные кандидата: {user}."

logger_start = "Разговор с пользователем {user} начался"
logger_end = "Разговор с пользователем {user} закончился"
logger_cancel = "Пользователь {user} отменил разговор"
