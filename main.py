#!/usr/bin/python3

from dotenv import load_dotenv
from bot_manager import BotManager
import os
import logging

def setup_logging():
    """
    Налаштовує логування для запису помилок у файл.

    Конфігурує базове логування, яке записує повідомлення рівня ERROR
    та вище у файл 'error.log'. Кожен запис буде містити час, рівень логування,
    і повідомлення помилки.
    """
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='error.log',
        filemode='a')

if __name__ == '__main__':
    setup_logging()
    load_dotenv()
    token = os.getenv("SHOP_BOT_TOKEN")
    bot_manager = BotManager(token)
    bot_manager.run()

