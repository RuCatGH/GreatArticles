import datetime
import html
import re

from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Prefetch
from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse, Http404
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.http import HttpResponse

from likes.services import get_fans
from .models import Article, Comment, Category
from .services import delete_article_comment, rename_comment_text, create_comment, add_ip_in_field_views, \
    get_latest_comments_list, get_popular_articles, get_paginator_for_page


def index(request) -> render:
    try:
        latest_articles_list = Article.objects.filter(is_published=True).order_by('-pub_date', 'id').prefetch_related(
            'views', Prefetch('comment', queryset=Comment.objects.all().only('id', 'article'))).only(
            'article_image', 'slug', 'article_title', 'article_text')
        popular = get_popular_articles()
        page_obj = get_paginator_for_page(latest_articles_list, request.GET.get('page'))
    except Article.DoesNotExist:
        raise Http404("Article not found")

    return render(request, 'articles/list.html', {'latest_articles_list': page_obj, 'popular': popular,
                                                  'title': 'Читайте интересные и познавательные статьи | GreatArticles'})


def detail(request, slug: str) -> render:
    try:
        response = HttpResponse("Cookies set")
        response.set_cookie('language', 'ru', samesite='Lax')

        ad_block = ('<div class="adblock-detail"><!-- Yandex.RTB R-A-2742101-6 --><div '
                    'id="yandex_rtb_R-A-2742101-6"></div><script>window.yaContextCb.push(()=>{	'
                    'Ya.Context.AdvManager.render({		"blockId": "R-A-2742101-6",		"renderTo": '
                    '"yandex_rtb_R-A-2742101-6"	})})</script></div>')

        article = Article.objects.filter(slug=slug, is_published=True).annotate(
            num_comments=Count('comment'), num_views=Count('views', distinct=True),
            num_likes=Count('likes', distinct=True)).select_related(
            'article_author', 'category').defer(
            'article_author__password', 'article_author__last_login', 'article_author__is_superuser',
            'article_author__username', 'article_author__first_name', 'article_author__last_name',
            'article_author__email',
            'article_author__is_staff', 'article_author__is_active', 'article_author__date_joined',
            'article_author__user_social', 'article_author__description', 'category__description',
            'category__keywords').get()

        h2_indices = [match.start() for match in re.finditer(r'<h2>', article.article_text)]

        # Если есть как минимум два <h2>, вставляем блок рекламы после второго <h2>
        if len(h2_indices) >= 2:
            second_h2_index = h2_indices[2]
            article.article_text = article.article_text[
                                    :second_h2_index + len("<h2>")] + ad_block + article.article_text[
                                                                                 second_h2_index + len("<h2>"):]

        ip = get_client_ip(request)

        category = Article.objects.get(slug=slug).category
        popular = get_popular_articles(detail=True, category=category)
        add_ip_in_field_views(ip, article)

        obj_type = ContentType.objects.get_for_model(Comment)
        if request.user.is_authenticated:
            latest_comments_list = get_latest_comments_list(obj_type, slug, request.user)
        else:
            latest_comments_list = get_latest_comments_list(obj_type, slug, None)
    except Article.DoesNotExist:
        raise Http404("Article not found")

    return render(request, 'articles/detail.html',
                  {'article': article, 'latest_comments_list': latest_comments_list, 'popular': popular})


def category(request, topics_slug: str) -> render:
    try:
        articles_category = Category.objects.get(slug=topics_slug)
        latest_articles_list = Article.objects.filter(category__slug=topics_slug, is_published=True).order_by(
            '-pub_date').prefetch_related(
            'views', Prefetch('comment', queryset=Comment.objects.all().only('id', 'article'))).only('article_image',
                                                                                                     'slug',
                                                                                                     'article_title',
                                                                                                     'article_text')
        popular = get_popular_articles(detail=True, category=articles_category)
        page_obj = get_paginator_for_page(latest_articles_list, request.GET.get('page'))
    except Article.DoesNotExist:
        raise Http404("Article not found")

    return render(request, 'articles/list.html',
                  {'latest_articles_list': page_obj, 'popular': popular, 'category': articles_category,
                   'title': f'{articles_category} - GreatArticles'})


@require_POST
def send_comment(request, slug: str) -> JsonResponse | HttpResponseBadRequest:
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.user.is_authenticated:
        comment_text = html.escape(request.POST['comment-text'].strip())
        user = request.user
        comment = create_comment(slug, request, comment_text, user)
        data = {
            'total_likes': get_fans(comment).count(),
            'comment_id': comment.id,
            'comment_author': str(comment.comment_author),
            'text': comment_text,
        }
        return JsonResponse(data)
    else:
        return HttpResponseBadRequest('Invalid request')


@require_POST
def delete_comment(request) -> JsonResponse | HttpResponseBadRequest:
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.user.is_authenticated:
        comment_id = request.POST['comment_id']
        delete_article_comment(id=comment_id)
        return JsonResponse({'status': 200, 'comment_id': comment_id})
    else:
        return HttpResponseBadRequest('Invalid request')


@require_POST
def edit_comment(request) -> JsonResponse | HttpResponseBadRequest:
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.user.is_authenticated:
        new_text = request.POST['new_text'].strip()
        rename_comment_text(id=request.POST['comment_id'], text=new_text)
        return JsonResponse({'new_text': new_text})
    else:
        return HttpResponseBadRequest('Invalid request')


def get_client_ip(request) -> str:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def articles_filter(request, pk: int) -> render:
    now = timezone.now()

    if pk == 'new':
        start_date = now - datetime.timedelta(days=7)
        latest_articles_list = Article.objects.filter(pub_date__gte=start_date, is_published=True).order_by('-pub_date').prefetch_related(
            'views',
            Prefetch('comment', queryset=Comment.objects.only('id', 'article'))
        ).only('article_image', 'slug', 'article_title', 'article_text')
    elif pk == 'week':
        start_date = now - datetime.timedelta(days=7)
        latest_articles_list = Article.objects.filter(pub_date__gte=start_date, is_published=True).annotate(
            total_views_count=Count('views')).order_by('-total_views_count').prefetch_related(
            Prefetch('comment', queryset=Comment.objects.only('id', 'article'))
        ).only('article_image', 'slug', 'article_title', 'article_text')
    elif pk == 'month':
        start_date = now - datetime.timedelta(days=30)
        latest_articles_list = Article.objects.filter(pub_date__gte=start_date, is_published=True).annotate(
            total_views_count=Count('views')).order_by('-total_views_count').prefetch_related(
            Prefetch('comment', queryset=Comment.objects.only('id', 'article'))
        ).only('article_image', 'slug', 'article_title', 'article_text')
    elif pk == 'alltime':
        latest_articles_list = Article.objects.filter(is_published=True).annotate(total_views_count=Count('views')).order_by(
            '-total_views_count').prefetch_related(
            Prefetch('comment', queryset=Comment.objects.only('id', 'article'))
        ).only('article_image', 'slug', 'article_title', 'article_text')
    else:
        raise Http404("Invalid filter option")

    popular = get_popular_articles()
    page_obj = get_paginator_for_page(latest_articles_list, request.GET.get('page'))

    return render(request, 'articles/list.html', {'latest_articles_list': page_obj, 'popular': popular, 'title': 'Читайте интересные и познавательные статьи | GreatArticles'})
