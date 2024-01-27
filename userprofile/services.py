from django.shortcuts import get_object_or_404

from userprofile.models import CustomUser


def edit_user_settings(user_id, request) -> None:
    """Изменение настроек пользователя"""
    user = get_object_or_404(CustomUser, id=user_id)
    user.nickname = request.POST['user_name'].strip()
    user.description = request.POST['description'].strip()
    user.user_social = request.POST['user_social'].strip()
    user.save()
