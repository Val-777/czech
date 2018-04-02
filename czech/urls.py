from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from quiz import views as quiz_views
from addwords import views as add_views
from accounts import views as accounts_views

urlpatterns = [
    path('', quiz_views.home, name='home'),
    path('api/addwords/', include('addwords.api.urls', namespace='addwords-api')),
    path('add/', add_views.add, name='add'),
    path('add/<slug:kind>/', add_views.add_word, name='add_word'),
    path('admin/', admin.site.urls),
    path('get_exercise/<slug:kind>/',
         quiz_views.get_exercise, name='get_exercise'),
    path('exercises/<slug:kind>/', quiz_views.exercise, name='exercise'),
    path('signup/', accounts_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html',
             email_template_name='accounts/password_reset_email.html',
             subject_template_name='accounts/password_reset_subject.txt'
         ), name='password_reset'),
    path('reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            auth_views.PasswordResetConfirmView.as_view(
                template_name='accounts/password_reset_confirm.html'),
            name='password_reset_confirm'),
    path('reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
    path('settings/password/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'),
         name='password_change'),
    path('settings/password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
         name='password_change_done'),
    path('settings/account/',
         accounts_views.UserUpdateView.as_view(), name='my_account'),
]
