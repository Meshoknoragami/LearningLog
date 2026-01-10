""" Определяет схемы URL для пользователей """

from django.urls import path, include

from . import views

app_name = 'users'
urlpatterns = [
    # включить URL авторизацию по умолчанию
    path('', include('django.contrib.auth.urls')),
    # страница выхода
    path('logged_out/', views.logout_view, name='logout'),
    # страница регистрации
    path('register/', views.register, name='register'),

]
