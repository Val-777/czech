"""
czech URL Configuration
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from quiz import views as quiz_views
from addwords import views as add_views

urlpatterns = [
    path('', quiz_views.home, name='home'),
    path('add/', add_views.add, name='add'),
    path('add_noun/', add_views.add_noun, name='add_noun'),
    path('add_verb/', add_views.add_verb, name='add_verb'),
    url(r'^admin/', admin.site.urls),
    path('get_exercise/<slug:kind>/',
         quiz_views.get_exercise, name='get_exercise'),
    path('exercises/<slug:kind>/', quiz_views.exercise, name='exercise'),
]
