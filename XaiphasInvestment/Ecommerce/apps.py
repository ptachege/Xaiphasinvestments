from django.apps import AppConfig


class EcommerceConfig(AppConfig):
    name = 'Ecommerce'


def ready(self):  # method just to import the signals
    import Ecommerce.signals
    import Ecommerce.views