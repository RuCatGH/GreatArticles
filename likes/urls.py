from django.urls import path
from . import views


app_name = 'likes'


urlpatterns = [
    path('add_like_article/', views.add_like_article, name='add_like_article'),  # Добавление лайка статьи
    path('remove_like_article/', views.remove_like_article, name='remove_like_article'),  # Удаление лайка статьи
    path('add_like_comment/', views.add_like_comment, name='add_like_comment'),  # Добавление лайка комментария
    path('remove_like_comment/', views.remove_like_comment, name='remove_like_comment'),  # Удаление лайка комментария
]
