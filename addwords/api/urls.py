from django.urls import path

from .views import (
    PersPronounListAPIView
)

app_name = 'addwords'

urlpatterns = [
    path('', PersPronounListAPIView.as_view(), name='list'),
]
