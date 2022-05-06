from django.apps import AppConfig


class CartnewConfig(AppConfig):
    name = 'cartnew'

    def ready(self):
        from cartnew import schedule_subscription_orders
        schedule_subscription_orders.start()