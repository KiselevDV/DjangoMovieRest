# import api

from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

# from .views import (
#     MovieListView, MovieDetailView, ActorsListView, ActorsDetailView,
#     ReviewCreateView, AddStarRatingView,
# )

from .views_set import (
    MovieViewSet, ActorsViewSet, ReviewCreateViewSet, AddStarRatingViewSet)

# app_name = 'movies'
# urlpatterns = [
#     path('movie/<int:pk>/', MovieDetailView.as_view()),
#     path('movie/', MovieListView.as_view()),
#     path('actors/<int:pk>/', ActorsDetailView.as_view()),
#     path('actors/', ActorsListView.as_view()),
#     path('review/', ReviewCreateView.as_view()),
#     path('rating/', AddStarRatingView.as_view()),
# ]

urlpatterns = format_suffix_patterns([
    path('movie/<int:pk>/', MovieViewSet.as_view({'get': 'retrieve'})),
    path('movie/', MovieViewSet.as_view({'get': 'list'})),
    path('actor/<int:pk>/', ActorsViewSet.as_view({'get': 'retrieve'})),
    path('actor/', ActorsViewSet.as_view({'get': 'list'})),
    path('review/', ReviewCreateViewSet.as_view({'post': 'create'})),
    path('rating/', AddStarRatingViewSet.as_view({'post': 'create'})),
])

# router = DefaultRouter()
# router.register(r'actor-set', api.ActorViewSet, basename='actor')
# router.register(r'actor-read', api.ActorReadOnly, basename='actor')
