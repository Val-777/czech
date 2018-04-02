from django.urls import path

from .views import (
    PersPronounCreateAPIView,
    PersPronounDeleteAPIView,
    PersPronounDetailAPIView,
    PersPronounListAPIView,
    PersPronounUpdateAPIView,
)

app_name = 'addwords'

urlpatterns = [
    path('', PersPronounListAPIView.as_view(), name='list'),
    path('create/', PersPronounCreateAPIView.as_view(), name='create'),
    path('<int:pk>/', PersPronounDetailAPIView.as_view(), name='detail'),
    path('<int:pk>/edit/', PersPronounUpdateAPIView.as_view(), name='update'),
    path('<int:pk>/delete/', PersPronounDeleteAPIView.as_view(), name='delete'),
]
