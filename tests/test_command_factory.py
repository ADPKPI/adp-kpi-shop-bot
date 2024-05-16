import pytest
from unittest.mock import MagicMock, patch
from command_factory import CommandFactory
from command_handlers import (
    ButtonHandler, ActiveOrdersCommand, TodayOrdersCommand, WeekOrdersCommand,
    MonthOrdersCommand, YearOrdersCommand, AllOrdersCommand, DetailsCommand,
    SetInProgressStatusCommand, SetDeliveryStatusCommand, SetProcessedStatusCommand,
    SetCanceledStatusCommand
)


@pytest.fixture
def factory():
    return CommandFactory()


def test_get_command(factory):
    assert isinstance(factory.get_command("active"), ActiveOrdersCommand)
    assert isinstance(factory.get_command("today"), TodayOrdersCommand)
    assert isinstance(factory.get_command("week"), WeekOrdersCommand)
    assert isinstance(factory.get_command("month"), MonthOrdersCommand)
    assert isinstance(factory.get_command("year"), YearOrdersCommand)
    assert isinstance(factory.get_command("all"), AllOrdersCommand)
    assert isinstance(factory.get_command("details"), DetailsCommand)
    assert isinstance(factory.get_command("set_in_progress_status"), SetInProgressStatusCommand)
    assert isinstance(factory.get_command("set_delivery_status"), SetDeliveryStatusCommand)
    assert isinstance(factory.get_command("set_processed_status"), SetProcessedStatusCommand)
    assert isinstance(factory.get_command("set_canceled_status"), SetCanceledStatusCommand)


def test_get_unknown_command(factory):
    with pytest.raises(ValueError) as exc_info:
        factory.get_command("unknown_command")
    assert str(exc_info.value) == "Unknown command: unknown_command"


def test_set_command_context(factory):
    mock_command = MagicMock()
    factory.set_command_context(mock_command)
    if hasattr(mock_command, 'set_factory'):
        mock_command.set_factory.assert_called_once_with(factory)



