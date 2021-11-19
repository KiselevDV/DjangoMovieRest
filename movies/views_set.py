"""
ReadOnlyModelViewSet - вывод списка и одной записи
"""
from django.db import models

from rest_framework.viewsets import (ReadOnlyModelViewSet, ModelViewSet)

from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Actor
from .serializers import (
    MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer,
    CreateRatingSerializer, ActorListSerializer, ActorDetailSerializer,
)
from .service import get_client_ip, MovieFilter, PaginationMovies


# То же через viewsets классы: ...
class ActorsViewSet(ReadOnlyModelViewSet):
    """Вывод всех актёров или режиссёров"""
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        # self.action - HTTP запросы
        if self.action == 'list':
            return ActorListSerializer
        elif self.action == 'retrieve':
            return ActorDetailSerializer


class MovieViewSet(ReadOnlyModelViewSet):
    """Вывод списка фильмов"""

    # Подключение фильтрации
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    pagination_class = PaginationMovies

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        elif self.action == 'retrieve':
            return MovieDetailSerializer


class ReviewCreateViewSet(ModelViewSet):
    """Добавление отзыва к фильму"""

    serializer_class = ReviewCreateSerializer


class AddStarRatingViewSet(ModelViewSet):
    """Добавление рейтинга к фильму"""

    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        """Добавить при сериализации"""
        serializer.save(ip=get_client_ip(self.request))
