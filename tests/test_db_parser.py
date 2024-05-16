import pytest
from unittest.mock import MagicMock, patch
from db_parser import DBParser, NewOrderInformation
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater
from config import shop_chats

@pytest.fixture
def mock_updater():
    updater = MagicMock(spec=Updater)
    updater.bot.send_message = MagicMock()
    return updater

@pytest.fixture
def mock_apiclient():
    with patch('db_parser.APIClient', autospec=True) as MockAPIClient:
        yield MockAPIClient

def test_db_parser_init(mock_updater, mock_apiclient):
    mock_apiclient.get_last_order_id.return_value = {'last_order_id': 1}
    parser = DBParser(mock_updater)
    assert parser.last_order_id == 1
    mock_apiclient.get_last_order_id.assert_called_once()

def test_fetch_new_orders(mock_updater, mock_apiclient):
    mock_apiclient.get_last_order_id.return_value = {'last_order_id': 1}
    mock_apiclient.fetch_new_orders.return_value = [(2,)]
    parser = DBParser(mock_updater)
    parser.fetch_new_orders()
    mock_apiclient.fetch_new_orders.assert_called_once_with(1)
    assert parser.last_order_id == 2
    mock_updater.bot.send_message.assert_called()

def test_new_order_information(mock_updater):
    order = 1
    command = NewOrderInformation()
    command.execute(order, mock_updater)
    for chat_id in shop_chats:
        mock_updater.bot.send_message.assert_any_call(
            chat_id=chat_id,
            text='Увага! Нове замовлення!',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Подивитися активні замовлення", callback_data="active")]
            ])
        )


