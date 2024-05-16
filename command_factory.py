from command_handlers import *

class CommandFactory:
    """
    Фабрика команд для створення та управління різними командами в системі.

    Використовує словник для зіставлення назв команд з функціями, які створюють
    екземпляри відповідних командних об'єктів.
    """
    def __init__(self):
        """
        Ініціалізація CommandFactory з попередньо визначеним словником команд.
        """
        self.command_map = {
            "button_handler": lambda: self.set_command_context(ButtonHandler()),
            "active": lambda: ActiveOrdersCommand(),
            "today": lambda: TodayOrdersCommand(),
            "week": lambda: WeekOrdersCommand(),
            "month": lambda: MonthOrdersCommand(),
            "year": lambda: YearOrdersCommand(),
            "all": lambda: AllOrdersCommand(),
            "details": lambda: DetailsCommand(),
            "set_in_progress_status": lambda: SetInProgressStatusCommand(),
            "set_delivery_status": lambda: SetDeliveryStatusCommand(),
            "set_processed_status": lambda: SetProcessedStatusCommand(),
            "set_canceled_status": lambda: SetCanceledStatusCommand(),
        }

    def set_command_context(self, command):
        """
        Встановлює контекст для команди, якщо це необхідно. Використовується у випадках, коли одна команда викликає іншу

        Параметри:
            command (Command): Командний об'єкт, для якого потрібно встановити контекст.

        Повертає:
            Command: Командний об'єкт з встановленим контекстом.
        """
        if hasattr(command, 'set_factory'):
            command.set_factory(self)
        return command

    def get_command(self, command_name):
        """
        Повертає екземпляр команди на основі її назви.

        Параметри:
            command_name (str): Назва команди для створення.

        Повертає:
            Command: Екземпляр команди.
        """
        command_constructor = self.command_map.get(command_name)
        if command_constructor:
            return command_constructor()
        else:
            raise ValueError(f"Unknown command: {command_name}")