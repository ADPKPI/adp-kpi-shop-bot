import schedule
import time
from datetime import datetime
from command_base import CommandBase
from telegram.ext import CallbackContext, Updater
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from command_factory import CommandFactory
from config import shop_chats
from db_manager import APIClient

class DBParser:
    """Клас для парсингу бази даних та обробки нових замовлень."""

    def __init__(self, updater: Updater):
        """Ініціалізує парсер з заданим Updater об'єктом."""
        self.last_order_id = APIClient.get_last_order_id()['last_order_id']
        self.updater = updater

    def fetch_new_orders(self):
        """Отримує нові замовлення з бази даних та надсилає повідомлення про них."""
        new_orders = [i[0] for i in APIClient.fetch_new_orders(self.last_order_id)]
        for order in new_orders:
            NewOrderInformation().execute(1, self.updater)
            self.last_order_id = int(order)

    def run(self):
        """Запускає парсер для регулярного отримання нових замовлень."""
        schedule.every(5).seconds.do(self.fetch_new_orders)

        while True:
            schedule.run_pending()
            time.sleep(1)

class NewOrderInformation(CommandBase):
    """Клас команди для інформування про нові замовлення."""

    def execute(self, order, updater: Updater):
        """Виконує команду, надсилаючи повідомлення про нове замовлення."""
        for chat_id in shop_chats:
            updater.bot.send_message(chat_id=chat_id, text=f'Увага! Нове замовлення!', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Подивитися активні замовлення", callback_data="active")]]))
