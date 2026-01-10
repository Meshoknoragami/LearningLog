"""Определяет схемы URL для learning_logs"""

from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
    # домашняя страница
    path('', views.index, name='index'),
    # страница со списком всех тем
    path('topics/', views.topics, name='topics'),
    # страница с подробной информацией по отдельной теме
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # страница для добавления новой темы
    path('new_topic/', views.new_topic, name='new_topic'),
    # страница для добавления новой записи
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    # страница для редактирования записи
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    # страница для редактирования названия темы
    path('edit_topic/<int:topic_id>/', views.edit_topic, name='edit_topic'),
    # страница для удаления темы
    path('delete_topic/<int:topic_id>/', views.delete_topic, name='delete_topic'),
    # страница для удаления записи
    path('delete_entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    # экспорт темы
    path('export_topic/<int:topic_id>/', views.export_topic, name='export_topic'),
    # пометка избранное
    path('toggle_bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    # страница избранное
    path('bookmarks/', views.bookmarks, name='bookmarks'),
]
