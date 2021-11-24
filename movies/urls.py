from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    MovieListView, MovieDetailView, ActorsListView, ActorsDetailView,
    ReviewCreateView, ReviewDestroyView, AddStarRatingView, )

from .views_set import (
    MovieViewSet, ActorsViewSet, ReviewCreateViewSet, AddStarRatingViewSet)

from . import api

app_name = 'movies'
# # Из views
# urlpatterns = [
#     path('movie/<int:pk>/', MovieDetailView.as_view()),
#     path('movie/', MovieListView.as_view()),
#     path('actors/<int:pk>/', ActorsDetailView.as_view()),
#     path('actors/', ActorsListView.as_view()),
#     path('review/<int:id>/', ReviewDestroyView.as_view()),
#     path('review/', ReviewCreateView.as_view()),
#     path('rating/', AddStarRatingView.as_view()),
# ]

# # Из views_set
# urlpatterns = format_suffix_patterns([
#     path('movie/<int:pk>/', MovieViewSet.as_view({'get': 'retrieve'})),
#     path('movie/', MovieViewSet.as_view({'get': 'list'})),
#     path('actor/<int:pk>/', ActorsViewSet.as_view({'get': 'retrieve'})),
#     path('actor/', ActorsViewSet.as_view({'get': 'list'})),
#     path('review/', ReviewCreateViewSet.as_view({'post': 'create'})),
#     path('rating/', AddStarRatingViewSet.as_view({'post': 'create'})),
# ])

#############################################################################
# # Из api № 1
# urlpatterns = [
#     path('actor-set/<int:pk>/', api.ActorViewSet.as_view({'get': 'retrieve'})),
#     path('actor-set/', api.ActorViewSet.as_view({'get': 'list'})),
# ]

# # Из api № 2
actor_list = api.ActorModelViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
actor_detail = api.ActorModelViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
actor_example = api.ActorModelViewSet.as_view({
    'get': 'example',
    'put': 'example'
})  # , renderer_classes=[renderers.JSONOpenAPIRenderer])
actor_my_list = api.ActorModelViewSet.as_view({
    'get': 'my_list',
    'post': 'create'
})

urlpatterns = format_suffix_patterns([
    path('actor/<int:pk>/example/', actor_example, name='actor-example'),
    path('actor/<int:pk>/', actor_detail, name='actor-detail'),
    path('actor/', actor_list, name='actor-list'),
    path('actor-my/', actor_my_list, name='actor-detail')
])

# Автоматическое генерирование уров через экземпляр DefaultRouter()
router = DefaultRouter()
# router.register(r'actor-set', api.ActorViewSet, basename='actor')
# router.register(r'actor-read', api.ActorReadOnly, basename='actor')
# router.register(r'actor-modelset', api.ActorModelViewSet, basename='actor')
# urlpatterns = router.urls
