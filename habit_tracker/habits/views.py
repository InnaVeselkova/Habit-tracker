from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Habit
from .serializers import HabitSerializer
from django.db import models


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, 'rest_framework.filters.OrderingFilter']
    filterset_fields = ['is_public', 'owner']
    ordering_fields = ['time', 'action']

    def get_queryset(self):
        user = self.request.user
        # Включаем все привычки пользователя + все публичные привычки других
        return Habit.objects.filter(
            models.Q(owner=user) | models.Q(is_public=True)
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def public_habits(self, request):
        # Показывает только публичные привычки
        queryset = Habit.objects.filter(is_public=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
