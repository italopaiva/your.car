from django.apps import AppConfig


class CarConfig(AppConfig):
    name = 'car'

    def ready(self):
        import yourcar.car.signals_handlers
