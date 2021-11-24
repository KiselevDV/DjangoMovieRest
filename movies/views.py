from django.db import models

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, )
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, )

from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Actor, Review
from .serializers import (
    MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer,
    CreateRatingSerializer, ActorListSerializer, ActorDetailSerializer,
)

from .permissions import IsSuperUser
from .service import get_client_ip, MovieFilter


# # Через базовый APIView
# class MovieListView(APIView):
#     """Вывод списка фильмов"""
#
#     def get(self, request):
#         # СПОСОБ № 1
#         # rating_user - установил ли данный пользователь рейтинг или нет
#         # Новое поле создаётся в сериализаторе, логика работы здесь
#         # movies = Movie.objects.filter(draft=False).annotate(
#         #     rating_user=models.Case(
#         #         # ratings - related_name, ip - поле модели Rating
#         #         # если запись есть возращаес значение True (then=True)
#         #         models.When(ratings__ip=get_client_ip(request), then=True),
#         #         default=False,  # если записи нет установить False
#         #         output_field=models.BooleanField()  # тип поля
#         #     )
#         # )
#
#         # СПОСОБ № 2
#         movies = Movie.objects.filter(draft=False).annotate(
#             rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(request)))
#         ).annotate(
#             middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
#         )
#         serializer = MovieListSerializer(movies, many=True)
#         return Response(serializer.data)
#
#
# class MovieDetailView(APIView):
#     """Вывод фильма"""
#
#     def get(self, request, pk):
#         movie = Movie.objects.get(id=pk, draft=False)
#         serializer = MovieDetailSerializer(movie)
#         return Response(serializer.data)
#
#
# class ReviewCreateView(APIView):
#     """Добавление отзыва к фильму"""
#
#     def post(self, request):
#         # request.data - данные из клиентского запроса
#         review = ReviewCreateSerializer(data=request.data)
#         if review.is_valid():
#             review.save()
#         return Response(status=201)
#
#
# class AddStarRatingView(APIView):
#     """Добавление рейтинга к фильму"""
#
#     def post(self, request):
#         serializer = CreateRatingSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(ip=get_client_ip(request))
#             return Response(status=201)
#         else:
#             return Response(status=400)

#########################################################################
# То же через generic классы: ListAPIView, RetrieveAPIView, CreateAPIView
class MovieListView(ListAPIView):
    """Вывод списка фильмов"""

    serializer_class = MovieListSerializer
    # Подключение фильтрации
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    # Права доступа
    permission_classes = (IsAuthenticated,)

    # authentication_classes = []

    # Логика добавление двух полей: rating_user, middle_star
    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies


class MovieDetailView(RetrieveAPIView):
    """Вывод фильма"""

    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class ReviewCreateView(CreateAPIView):
    """Добавление отзыва к фильму"""

    serializer_class = ReviewCreateSerializer
    permission_classes = (IsAdminUser,)  # только суперпользователь


class ReviewDestroyView(DestroyAPIView):
    """Удалить отзыв"""
    queryset = Review.objects.all()
    permission_classes = (IsSuperUser,)  # только суперпользователь


class AddStarRatingView(CreateAPIView):
    """Добавление рейтинга к фильму"""

    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        """Добавить при сериализации"""
        serializer.save(ip=get_client_ip(self.request))


class ActorsListView(ListAPIView):
    """Вывод всех актёров или режиссёров"""
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorsDetailView(RetrieveAPIView):
    """Вывод актёра или режиссёра"""
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
