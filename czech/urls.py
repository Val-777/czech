from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from quiz import views as quiz_views
from addwords import views as add_views
from accounts import views as accounts_views

urlpatterns = [
    path('', quiz_views.home, name='home'),
    path('add/', add_views.add, name='add'),
    path('add/<slug:kind>/', add_views.add_word, name='add_word'),
    path('admin/', admin.site.urls),
    path('get_exercise/<slug:kind>/',
         quiz_views.get_exercise, name='get_exercise'),
    path('exercises/<slug:kind>/', quiz_views.exercise, name='exercise'),
    path('signup/', accounts_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
