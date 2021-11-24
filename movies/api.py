from django.shortcuts import get_object_or_404

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.renderers import AdminRenderer
from rest_framework.response import Response
from rest_framework.viewsets import (
    ViewSet, ReadOnlyModelViewSet, ModelViewSet, )

from .models import Actor
from .serializers import (ActorListSerializer, ActorDetailSerializer, )


class ActorViewSet(ViewSet):
    def list(self, request):
        """Все актёры и режиссёры"""
        queryset = Actor.objects.all()
        serializer = ActorListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Детально об актёре или режиссёре"""
        queryset = Actor.objects.all()
        actor = get_object_or_404(queryset, pk=pk)
        serializer = ActorDetailSerializer(actor)
        return Response(serializer.data)


class ActorReadOnly(ReadOnlyModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorModelViewSet(ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer

    @action(detail=False, permission_classes=[IsAuthenticated])
    def my_list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['get', 'put'], renderer_classes=[AdminRenderer])
    def example(self, request, *args, **kwargs):
        """Пример добавления своего метода"""
        actor = self.get_object()
        serializer = ActorDetailSerializer(actor)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'example':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
