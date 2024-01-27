from django.urls import path, include
from . import views
from .feeds import LatestPostsFeed

app_name = 'articles'

urlpatterns = [
    path('delete_comment/', views.delete_comment, name='delete_comment'),  # Удаление комментария
    path('edit_comment/', views.edit_comment, name='edit_comment'),  # Редактирование комментария
    path('<slug:slug>/', views.detail, name='detail'),  # Страница с новостью
    path('topics/<slug:topics_slug>', views.category, name='category'),
    path('filter/<str:pk>', views.articles_filter, name='articles_filter'),  # Фильтр по категориям
    path('<slug:slug>/send_comment', views.send_comment, name='send_comment'),  # Отправка комментария
    path('feed/rss', LatestPostsFeed(), name="post_feed"),
    path('', views.index, name='index'),  # Главная страница
]
