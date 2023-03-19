import logging
import os


formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(name)s - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler(filename="logs.log", mode="a")
file_handler.setFormatter(formatter)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

file_storage = os.path.join(BASE_DIR, "recruiter_bot/data/Кандидаты.txt")
