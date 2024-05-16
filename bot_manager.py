from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from command_factory import CommandFactory
from db_parser import DBParser
from threading import Thread


class BotManager:
    """
    Керує всіма аспектами бота Telegram, включаючи ініціалізацію та обробку повідомлень.

    Використовує CommandFactory для управління командами, що відповідають на різні типи запитів.
    """
    def __init__(self, token):
        """
        Керує всіма аспектами бота Telegram, включаючи ініціалізацію та обробку повідомлень.

        Використовує CommandFactory для управління командами, що відповідають на різні типи запитів.
        """
        self.updater = Updater(token, use_context=True)
        self.parser = DBParser(self.updater)
        self._register_handlers()

    def _register_handlers(self):
        """
        Реєструє обробники команд для різних типів повідомлень та запитів.
        """
        self.factory = CommandFactory()
        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", lambda u, c: self.factory.get_command("start").execute(u, c)))
        dispatcher.add_handler(CommandHandler("active", lambda u, c: self.factory.get_command("active").execute(u, c), pass_args=True))
        dispatcher.add_handler(CommandHandler("today", lambda u, c: self.factory.get_command("today").execute(u, c), pass_args=True))
        dispatcher.add_handler(CommandHandler("week", lambda u, c: self.factory.get_command("week").execute(u, c), pass_args=True))
        dispatcher.add_handler(CommandHandler("month", lambda u, c: self.factory.get_command("month").execute(u, c), pass_args=True))
        dispatcher.add_handler(CommandHandler("year", lambda u, c: self.factory.get_command("year").execute(u, c), pass_args=True))
        dispatcher.add_handler(CommandHandler("all", lambda u, c: self.factory.get_command("all").execute(u, c), pass_args=True))
        dispatcher.add_handler(CallbackQueryHandler(lambda u, c: self.factory.get_command("button_handler").execute(u, c)))
        dispatcher.add_handler(CommandHandler("list", lambda u, c: self.factory.get_command("list").execute(u, c), pass_args=True))

    def run(self):
        """
        Запускає бота та входить в режим очікування повідомлень.
        """
        parser_thread = Thread(target=self.parser.run)
        parser_thread.start()

        self.updater.start_polling()
        self.updater.idle()





