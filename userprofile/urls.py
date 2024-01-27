from django.urls import path
from . import views

app_name = 'userprofile'

urlpatterns = [
    path('', views.view_profile, name='profile'),  # Страница с профилем
    path('save_user_settings/<int:user_id>', views.save_user_settings, name='save_user_settings')
]
