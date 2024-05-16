from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from command_base import CommandBase
import logging
from prettytable import PrettyTable
import ast
from io import BytesIO
from datetime import datetime, timedelta
from db_manager import APIClient

class ActiveOrdersCommand(CommandBase):
    """Клас команди для отримання активних замовлень."""

    def execute(self, update: Update, context: CallbackContext):
        """Виконує команду, надсилаючи повідомлення з активними замовленнями."""
        try:
            rows = APIClient.get_active_orders()

            keyboard = [[InlineKeyboardButton(f'#{row[0]} | {row[1]}', callback_data=row[0])] for row in rows]
            reply_markup = InlineKeyboardMarkup(keyboard)

            context.bot.send_message(chat_id=update.effective_chat.id, text='Активні замовлення:',
                                     parse_mode='HTML', reply_markup=reply_markup)
        except Exception as e:
            logging.error(f"Active Orders Command execute error: {e}", exc_info=True)

class TodayOrdersCommand(CommandBase):
    """Клас команди для отримання замовлень за сьогодні."""

    def execute(self, update: Update, context: CallbackContext):
        """Виконує команду, надсилаючи повідомлення з замовленнями за сьогодні."""
        try:
            rows = APIClient.get_orders_today()

            keyboard = [[InlineKeyboardButton(f'#{row[0]} | {row[1]}', callback_data=row[0])] for row in rows]
            reply_markup = InlineKeyboardMarkup(keyboard)

            context.bot.send_message(chat_id=update.effective_chat.id, text='Замовлення за сьогодні:',
                                     parse_mode='HTML', reply_markup=reply_markup)
        except Exception as e:
            logging.error(f"Today Orders Command execute error: {e}", exc_info=True)

class WeekOrdersCommand(CommandBase):
    """Клас команди для отримання замовлень за тиждень."""

    def execute(self, update: Update, context: CallbackContext):
        """Виконує команду, надсилаючи повідомлення з замовленнями за тиждень."""
        try:
            rows = APIClient.get_orders_last_week()

            keyboard = [[InlineKeyboardButton(f'#{row[0]} | {row[1]}', callback_data=row[0])] for row in rows]
            reply_markup = InlineKeyboardMarkup(keyboard)

            context.bot.send_message(chat_id=update.effective_chat.id, text='Замовлення за тиждень:',
                                     parse_mode='HTML', reply_markup=reply_markup)
        except Exception as e:
            logging.error(f"Week Orders Command execute error: {e}", exc_info=True)

class MonthOrdersCommand(CommandBase):
    """Клас команди для отримання замовлень за місяць."""

    def execute(self, update: Update, context: CallbackContext):
        """Виконує команду, надсилаючи повідомлення з замовленнями за місяць."""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')

            orders = APIClient.get_orders_last_month()
            SendOrdersReportCommand.execute(orders, start_date_str, end_date_str, update, context)

        except Exception as e:
            logging.error(f"Month Orders Command execute error: {e}")

class YearOrdersCommand(CommandBase):
    """Клас команди для отримання замовлень за рік."""

    def execute(self, update: Update, context: CallbackContext):
        """Виконує команду, надсилаючи повідомлення з замовленнями за рік."""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)
            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')

            orders = APIClient.get_orders_last_year()
            SendOrdersReportCommand.execute(orders, start_date_str, end_date_str, update, context)

        except Exception as e:
            logging.error(f"Year Orders Command execute error: {e}")

class AllOrdersCommand(CommandBase):
    """Клас команди для отримання всіх замовлень."""

    def execute(self, update: Update, context: CallbackContext):
        """Виконує команду, надсилаючи повідомлення з усіма замовленнями."""
        try:
            end_date = datetime.now()
            start_date_str = '2024-03-14'
            end_date_str = end_date.strftime('%Y-%m-%d')

            orders = APIClient.get_all_orders()
            SendOrdersReportCommand.execute(orders, start_date_str, end_date_str, update, context)

        except Exception as e:
            logging.error(f"All Orders Command execute error: {e}")

class SendOrdersReportCommand(CommandBase):
    """Клас команди для відправки звіту про замовлення."""

    def execute(orders, start, end, update, context):
        """Виконує команду, надсилаючи файл з замовленнями."""
        file_content = ''
        for order_details in orders:
            order_list = PrettyTable()
            order_list.field_names = ["Назва", "N", "Сума"]
            order_list.add_rows(ast.literal_eval(order_details[3]))

            location = order_details[6].split("|") if order_details and order_details[6] else (0, 0)
            latitude, longitude = map(float, location)

            file_content += f'-------------------------------------------' \
                            f'\nЗамовлення №{order_details[0]}:\nCтатус: {order_details[7]}\n{order_list}\nСума: ' \
                            f'{order_details[4]}\nНомер телефону: {order_details[2]}\nЧас замовлення: ' \
                            f'{order_details[5]}\nАдреса:{latitude};{longitude}' \
                            f'\n-------------------------------------------\n\n\n\n\n'
        with BytesIO(file_content.encode('utf-8')) as file:
            file.name = "month_orders.txt"
            file.seek(0)
            context.bot.send_document(chat_id=update.effective_chat.id, document=file,
                                      filename=f"Замовлення {start} - {end}.txt")

class DetailsCommand(CommandBase):
    """Клас команди для отримання деталей замовлення."""

    def execute(self, update: Update, context: CallbackContext, order_id=None):
        """Виконує команду, надсилаючи детальну інформацію про замовлення."""
        try:
            if order_id is None: order_id = ' '.join(context.args)
            context.user_data['current_order_id'] = int(order_id)

            order_details = APIClient.get_order_details(order_id)[0]

            order_list = PrettyTable()
            order_list.field_names = ["Назва", "N", "Сума"]
            order_list.add_rows(ast.literal_eval(order_details[3]))

            location = order_details[6].split("|") if order_details and order_details[6] else (0, 0)
            latitude, longitude = map(float, location)

            output = f'Замовлення №{order_id}:\n\nCтатус: {order_details[7]}\n\n<code>{order_list}</code>\n\nСума: {order_details[4]}\n\nНомер телефону: {order_details[2]}\nЧас замовлення: {order_details[5]}\n\nАдреса:'

            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton("Змінити статус: In Progress", callback_data="set_in_progress_status")],
                 [InlineKeyboardButton("Змінити статус: Delivery", callback_data="set_delivery_status")],
                 [InlineKeyboardButton("Змінити статус: Processed", callback_data="set_processed_status")],
                 [InlineKeyboardButton("Змінити статус: Canceled", callback_data="set_canceled_status")]]
            )

            context.bot.send_message(chat_id=update.effective_chat.id, text=output,
                                     parse_mode='HTML')
            context.bot.send_location(chat_id=update.effective_chat.id, latitude=latitude, longitude=longitude, reply_markup=keyboard)
        except Exception as e:
            logging.error(f"Details Command execute error: {e}", exc_info=True)

class SetInProgressStatusCommand(CommandBase):
    """Клас команди для зміни статусу замовлення на 'In Progress'."""

    def execute(self, update: Update, context: CallbackContext):
        """Виконує команду, змінюючи статус замовлення на 'In Progress'."""
        try:
            order_id = context.user_data['current_order_id']
            if int(order_id) > 0:
                APIClient.change_order_status(order_id, 'In Progress')
                context.user_data['current_order_id'] = -1
                context.bot.send_message(chat_id=update.effective_chat.id, text=f'Замовлення №{order_id} --- Новий статус: In Progress')
        except Exception as e:
            logging.error(f"Set In Progress Status Command execute error: {e}", exc_info=True)

class SetDeliveryStatusCommand(CommandBase):
    """Клас команди для зміни статусу замовлення на 'Delivery'."""

    def execute(self, update: Update, context: CallbackContext):
        """Виконує команду, змінюючи статус замовлення на 'Delivery'."""
        try:
            order_id = context.user_data['current_order_id']
            if int(order_id) > 0:
                APIClient.change_order_status(order_id, 'Delivery')
                context.user_data['current_order_id'] = -1
                context.bot.send_message(chat_id=update.effective_chat.id, text=f'Замовлення №{order_id} --- Новий статус: Delivery')
        except Exception as e:
            logging.error(f"Set Delivery Status Command execute error: {e}")
        context.user_data['current_order_id'] = -1

class SetProcessedStatusCommand(CommandBase):
    """Клас команди для зміни статусу замовлення на 'Processed'."""

    def execute(self, update: Update, context: CallbackContext):
        """Виконує команду, змінюючи статус замовлення на 'Processed'."""
        try:
            order_id = context.user_data['current_order_id']
            if int(order_id) > 0:
                APIClient.change_order_status(order_id, 'Processed')
                context.user_data['current_order_id'] = -1
                context.bot.send_message(chat_id=update.effective_chat.id, text=f'Замовлення №{order_id} --- Новий статус: Processed')
        except Exception as e:
            logging.error(f"Set Processed Status Command execute error: {e}", exc_info=True)

class SetCanceledStatusCommand(CommandBase):
    """Клас команди для зміни статусу замовлення на 'Canceled'."""

    def execute(self, update: Update, context: CallbackContext):
        """Виконує команду, змінюючи статус замовлення на 'Canceled'."""
        try:
            order_id = context.user_data['current_order_id']
            if int(order_id) > 0:
                APIClient.change_order_status(order_id, 'Canceled')
                context.user_data['current_order_id'] = -1
                context.bot.send_message(chat_id=update.effective_chat.id, text=f'Замовлення №{order_id} --- Новий статус: Canceled')

        except Exception as e:
            logging.error(f"Set Canceled Status Command execute error: {e}", exc_info=True)
        context.user_data['current_order_id'] = -1

class ButtonHandler(CommandBase):
    """Клас обробника кнопок, що викликає відповідні команди."""

    def set_factory(self, factory):
        """Встановлює фабрику команд."""
        self.command_factory = factory

    def execute(self, update: Update, context: CallbackContext):
        """Виконує команду, яка обробляє натиснуті кнопки."""
        try:
            query = update.callback_query
            query.answer()
            callback_data = query.data
            try:
                command = self.command_factory.get_command(callback_data)
                command.execute(update, context)
            except:
                context.args = [callback_data]
                command = self.command_factory.get_command("details")
                command.execute(update, context)
        except Exception as e:
            logging.error(f"Button Handler execute error: {e}", exc_info=True)
