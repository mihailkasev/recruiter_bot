FROM python:3.9-slim AS bot

WORKDIR /recruiter_bot
COPY requirements.txt .

# для быстрого запуска и проверки бота убрал команды обновления пакетов
# RUN apt-get update \
#     && apt install -y --no-install-recommends --no-install-suggests build-essential python3-pip python3-venv

RUN pip install --no-cache-dir --upgrade pip \
    && pip install -r requirements.txt --no-cache-dir

COPY . .

CMD python3 run_polling.py
