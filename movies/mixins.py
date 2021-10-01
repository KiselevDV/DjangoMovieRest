"""
Миксины

В шаблонах добавляет переменную view, через которую осуществляется
обращение к методам - view.get_genres или view.get_years
"""
from .models import Genre, Movie


class GenreYear:
    """Жанры и года выхода фильмов"""

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        # values('year') - забрать только записи лет, а не фильмов целиком
        return Movie.objects.filter(draft=False).values("year")
