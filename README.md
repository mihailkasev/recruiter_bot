# Telegram бот для найма сотрудников

### Описание
- Telegram бот для получения информации о кандидате.
- Проект реализован на базе асинхронной библиотеки python-telegram-bot v20.1 с использованием базы данных MongoDB.
- Проект запускается в двух docker-контейнерах (bot, db).

### Технологии
- Python 3.9.10
- python-telegram-bot 20.1
- python-dotenv 1.0.0
- motor 3.1.1

### Запуск проекта
- Подключить telegram бота через [BotFather](https://t.me/BotFather) и получить Token.
- Клонировать репозиторий:
```
git clone https://github.com/mihailkasev/recruiter_bot
```
- Перейти в папку infra:
```
cd infra
```
- Создать файл с переменными окружения .env и заполнить данными:
```
TELEGRAM_TOKEN=<Полученный токен telegram бота>
MONGO=db  # по названию контейнера
ADMIN_ID=<telegram id>  # telegram id пользователя-администратора
```
- Запустить контейнеры:
```
docker-compose up
```
### Бот готов к работе!

### Полезные команды:
- /start - запустить бота
- /cancel - отменить разговор
- /export_users - скачать файл с данными кандидатов
- /message - отправить сообщение определенному кандидату

### Автор:
- [Михаил Касев](https://github.com/mihailkasev/)
