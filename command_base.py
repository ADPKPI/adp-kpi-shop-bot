from telegram import Update
from telegram.ext import CallbackContext

class CommandBase:
    """
    Абстрактний базовий клас для всіх команд бота.

    Визначає інтерфейс для виконання команд, що мають бути імплементовані
    в похідних класах.
    """
    def execute(self, update: Update, context: CallbackContext):
        """
        Абстрактний базовий клас для всіх команд бота.

        Визначає інтерфейс для виконання команд, що мають бути імплементовані
        в похідних класах.
        """
        raise NotImplementedError