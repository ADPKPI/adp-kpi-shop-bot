import pytest
from unittest.mock import MagicMock, patch
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from command_handlers import (
    ActiveOrdersCommand, TodayOrdersCommand, WeekOrdersCommand,
    MonthOrdersCommand, YearOrdersCommand, AllOrdersCommand, DetailsCommand,
    SetInProgressStatusCommand, SetDeliveryStatusCommand, SetProcessedStatusCommand,
    SetCanceledStatusCommand, ButtonHandler
)

@pytest.fixture
def mock_update():
    return MagicMock(spec=Update)

@pytest.fixture
def mock_context():
    context = MagicMock(spec=CallbackContext)
    context.bot.send_message = MagicMock()
    context.bot.send_document = MagicMock()
    return context

@pytest.fixture
def mock_apiclient():
    with patch('command_handlers.APIClient', autospec=True) as MockAPIClient:
        yield MockAPIClient

def test_active_orders_command(mock_update, mock_context, mock_apiclient):
    mock_apiclient.get_active_orders.return_value = [(1, 'Order1'), (2, 'Order2')]
    command = ActiveOrdersCommand()
    command.execute(mock_update, mock_context)
    mock_context.bot.send_message.assert_called_once()
    mock_apiclient.get_active_orders.assert_called_once()

def test_today_orders_command(mock_update, mock_context, mock_apiclient):
    mock_apiclient.get_orders_today.return_value = [(1, 'Order1'), (2, 'Order2')]
    command = TodayOrdersCommand()
    command.execute(mock_update, mock_context)
    mock_context.bot.send_message.assert_called_once()
    mock_apiclient.get_orders_today.assert_called_once()

def test_week_orders_command(mock_update, mock_context, mock_apiclient):
    mock_apiclient.get_orders_last_week.return_value = [(1, 'Order1'), (2, 'Order2')]
    command = WeekOrdersCommand()
    command.execute(mock_update, mock_context)
    mock_context.bot.send_message.assert_called_once()
    mock_apiclient.get_orders_last_week.assert_called_once()

def test_month_orders_command(mock_update, mock_context, mock_apiclient):
    mock_apiclient.get_orders_last_month.return_value = [(1, 'Order1'), (2, 'Order2')]
    command = MonthOrdersCommand()
    command.execute(mock_update, mock_context)
    mock_apiclient.get_orders_last_month.assert_called_once()

def test_year_orders_command(mock_update, mock_context, mock_apiclient):
    mock_apiclient.get_orders_last_year.return_value = [(1, 'Order1'), (2, 'Order2')]
    command = YearOrdersCommand()
    command.execute(mock_update, mock_context)
    mock_apiclient.get_orders_last_year.assert_called_once()

def test_all_orders_command(mock_update, mock_context, mock_apiclient):
    mock_apiclient.get_all_orders.return_value = [(1, 'Order1'), (2, 'Order2')]
    command = AllOrdersCommand()
    command.execute(mock_update, mock_context)
    mock_apiclient.get_all_orders.assert_called_once()

def test_details_command(mock_update, mock_context, mock_apiclient):
    mock_apiclient.get_order_details.return_value = [(1, 'Order1')]
    command = DetailsCommand()
    command.execute(mock_update, mock_context, order_id=1)
    mock_apiclient.get_order_details.assert_called_once()

def test_set_in_progress_status_command(mock_update, mock_context, mock_apiclient):
    command = SetInProgressStatusCommand()
    mock_context.user_data = {'current_order_id': 1}
    command.execute(mock_update, mock_context)
    mock_apiclient.change_order_status.assert_called_once_with(1, 'In Progress')

def test_set_delivery_status_command(mock_update, mock_context, mock_apiclient):
    command = SetDeliveryStatusCommand()
    mock_context.user_data = {'current_order_id': 1}
    command.execute(mock_update, mock_context)
    mock_apiclient.change_order_status.assert_called_once_with(1, 'Delivery')

def test_set_processed_status_command(mock_update, mock_context, mock_apiclient):
    command = SetProcessedStatusCommand()
    mock_context.user_data = {'current_order_id': 1}
    command.execute(mock_update, mock_context)
    mock_apiclient.change_order_status.assert_called_once_with(1, 'Processed')

def test_set_canceled_status_command(mock_update, mock_context, mock_apiclient):
    command = SetCanceledStatusCommand()
    mock_context.user_data = {'current_order_id': 1}
    command.execute(mock_update, mock_context)
    mock_apiclient.change_order_status.assert_called_once_with(1, 'Canceled')

def test_button_handler_command(mock_update, mock_context, mock_apiclient):
    factory = MagicMock()
    mock_update.callback_query.data = 'details'
    command = ButtonHandler()
    command.set_factory(factory)
    command.execute(mock_update, mock_context)
    factory.get_command.assert_called_once_with('details')
    factory.get_command.return_value.execute.assert_called_once()
