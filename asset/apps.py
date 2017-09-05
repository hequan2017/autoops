from django.apps import AppConfig
from suit.apps import DjangoSuitConfig

class AssetConfig(AppConfig):
    name = 'asset'

class SuitConfig(DjangoSuitConfig):
    layout = 'vertical'