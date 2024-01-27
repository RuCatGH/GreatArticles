from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from articles.models import Article, Comment
from .models import Like

User = get_user_model()


def get_comment(comment_id: str) -> object:
    return Comment.objects.only('id').get(id=comment_id)


def get_article(article_id: str) -> object:
    return Article.objects.only('id').get(id=article_id)


def add_like(obj, user) -> object:
    """Лайкает `obj`."""
    obj_type = ContentType.objects.get_for_model(obj)
    like, is_created = Like.objects.get_or_create(
        content_type=obj_type, object_id=obj.id, user=user)
    return like


def remove_like(obj, user) -> None:
    """Удаляет лайк с `obj`."""
    obj_type = ContentType.objects.get_for_model(obj)
    Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user
    ).delete()


def is_fan(obj, user) -> bool:
    """Проверяет, лайкнул ли `user` `obj`."""
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    likes = Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user)
    return likes.exists()


def get_fans(obj) -> object:
    """Получает всех пользователей, которые лайкнули `obj`.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    return User.objects.filter(
        likes__content_type=obj_type, likes__object_id=obj.id).only('id')
