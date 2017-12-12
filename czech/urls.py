"""czech URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from quiz import views as quiz_views

urlpatterns = [
    url(r'^$', quiz_views.home, name='home'),
    url(r'^add/', quiz_views.add, name='add'),
    url(r'^add_noun/', quiz_views.add_noun, name='add_noun'),
    url(r'^admin/', admin.site.urls),
    url(r'^ajax/get_exercise', quiz_views.get_exercise, name='get_exercise'),
]
