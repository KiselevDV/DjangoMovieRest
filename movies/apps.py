"""
Для настройки приложения, выставления некоторых его атрибутов
"""
from django.apps import AppConfig


class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'
    verbose_name = 'Фильмы'
