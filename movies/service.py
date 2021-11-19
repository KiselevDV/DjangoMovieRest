from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from django_filters import rest_framework as filters

from .models import Movie


def get_client_ip(request):
    """Получить ip адрес пользователя"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    """
    Для объединения разных фильтров.
    BaseInFilter - использовать in для фильтрации.
    CharFilter - фильтрация по имени
    """
    pass


class MovieFilter(filters.FilterSet):
    """Фильтрация списка фильмов по годам и жанрам"""
    genres = CharFilterInFilter(field_name='genres__name', lookup_expr='in')
    year = filters.RangeFilter()  # диапазон

    class Meta:
        model = Movie
        fields = ['genres', 'year']


class PaginationMovies(PageNumberPagination):
    page_size = 2
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })
