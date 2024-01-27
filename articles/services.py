from django.core.paginator import Paginator
from django.db.models import Prefetch, When, Exists, Value, OuterRef, BooleanField, Case, Count

from articles.models import Comment, Article, Ip
from likes.models import Like


def get_paginator_for_page(latest_articles_list, page_number: int) -> object:
    paginator = Paginator(latest_articles_list, 10)
    page_obj = paginator.get_page(page_number)
    return page_obj


def get_popular_articles(detail=False, category=False) -> object:
    if detail:
        return Article.objects.annotate(num_comments=Count('comment'),
                                        num_views=Count('views', distinct=True)).filter(category=category).only(
            'article_title', 'slug').order_by('-pub_date')[:4]
    else:
        return Article.objects.filter(is_published=True).annotate(num_comments=Count('comment'),
                                                                  num_views=Count('views', distinct=True)).all().only(
            'article_title', 'slug').order_by('-pub_date')[:4]


def get_latest_comments_list(obj_type, slug: str, user) -> list:
    latest_comments_list = Comment.objects.filter(reply=None) \
                               .select_related('article') \
                               .filter(article__slug=slug) \
                               .select_related('comment_author').prefetch_related(
        Prefetch('replies', queryset=Comment.objects.select_related('comment_author').annotate(is_reply_liked=Case(
            When(Exists(Like.objects.filter(content_type=obj_type, object_id=OuterRef('id'), user=user)),
                 then=Value(True)), default=Value(False), output_field=BooleanField()),
            num_reply_comment_likes=Count('likes', distinct=True)).only('comment_author',
                                                                        'comment_date',
                                                                        'comment_text',
                                                                        'comment_author__avatar',
                                                                        'comment_author__nickname',
                                                                        'reply'))) \
                               .annotate(num_replies=Count('replies'), num_comment_likes=Count('likes', distinct=True),
                                         is_liked=Case(
                                             When(Exists(
                                                 Like.objects.filter(content_type=obj_type, object_id=OuterRef('id'),
                                                                     user=user)),
                                                 then=Value(True)), default=Value(False), output_field=BooleanField())) \
                               .only('article__slug', 'comment_text', 'comment_date', 'comment_author__avatar',
                                     'comment_author__nickname') \
                               .order_by('-id')[:50]
    return latest_comments_list


def delete_article_comment(id: int) -> None:
    """Удаление комментария статьи"""
    Comment.objects.only('id').get(id=id).delete()


def rename_comment_text(id: int, text: str) -> None:
    """Изменение текста комментария"""
    comment = Comment.objects.only('comment_text').get(id=id)
    comment.comment_text = text
    comment.save()


def create_comment(slug: str, request, text: str, user: str) -> tuple[object, str]:
    """Создание комментария"""
    article = Article.objects.only('id').get(slug=slug)
    try:
        parent_id = request.POST['parent_id']
        parent = article.comment.get(id=parent_id)
        comment = article.comment.create(comment_text=text, comment_author=user, reply=parent)
    except:
        comment = article.comment.create(comment_text=text, comment_author=user)
    return comment


def add_ip_in_field_views(ip: str, article: object) -> None:
    """Добавление ip в поле views модели article"""
    if Ip.objects.filter(ip=ip).exists():
        article.views.add(Ip.objects.get(ip=ip))
    else:
        Ip.objects.create(ip=ip)
        article.views.add(Ip.objects.get(ip=ip))


