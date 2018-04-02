from django.urls import path

from .views import (
    PersPronounListAPIView,
    PersPronounDetailAPIView,
)

app_name = 'addwords'

urlpatterns = [
    path('', PersPronounListAPIView.as_view(), name='list'),
    path('<int:pk>/', PersPronounDetailAPIView.as_view(), name='detail'),
]
