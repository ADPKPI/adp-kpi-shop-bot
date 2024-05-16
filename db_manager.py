import requests
from config import api_url

class APIClient:
    """Клас клієнта API для взаємодії з сервером замовлень."""

    @classmethod
    def get_active_orders(cls):
        """Отримує список активних замовлень з API."""
        return requests.get(f"{api_url}/orders/active").json()

    @classmethod
    def get_orders_today(cls):
        """Отримує список замовлень, створених сьогодні, з API."""
        return requests.get(f"{api_url}/orders/today").json()

    @classmethod
    def get_orders_last_week(cls):
        """Отримує список замовлень за останній тиждень з API."""
        return requests.get(f"{api_url}/orders/last-week").json()

    @classmethod
    def get_orders_last_month(cls):
        """Отримує список замовлень за останній місяць з API."""
        return requests.get(f"{api_url}/orders/last-month").json()

    @classmethod
    def get_orders_last_year(cls):
        """Отримує список замовлень за останній рік з API."""
        return requests.get(f"{api_url}/orders/last-year").json()

    @classmethod
    def get_all_orders(cls):
        """Отримує список усіх замовлень з API."""
        return requests.get(f"{api_url}/orders/all").json()

    @classmethod
    def get_order_details(cls, order_id):
        """Отримує детальну інформацію про замовлення за ідентифікатором з API."""
        return requests.get(f"{api_url}/orders/details/{order_id}").json()

    @classmethod
    def change_order_status(cls, order_id, status):
        """Змінює статус замовлення за ідентифікатором через API."""
        data = {'order_id': order_id, 'status': status}
        return requests.patch(f"{api_url}/orders/change-status", json=data).json()

    @classmethod
    def get_last_order_id(cls):
        """Отримує ідентифікатор останнього замовлення з API."""
        return requests.get(f"{api_url}/orders/last-order-id").json()

    @classmethod
    def fetch_new_orders(cls, last_order_id):
        """Отримує нові замовлення з API, починаючи з вказаного ідентифікатора замовлення."""
        return requests.get(f"{api_url}/orders/fetch-new/{last_order_id}").json()
