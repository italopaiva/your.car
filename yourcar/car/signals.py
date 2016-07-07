from django.dispatch import Signal

car_refuel_expense = Signal(providing_args=["car"])