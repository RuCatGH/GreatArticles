from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_POST

from likes.services import add_like, remove_like, get_fans, get_article, get_comment


# Добавление лайка для статьи
@require_POST
def add_like_article(request) -> JsonResponse | HttpResponseBadRequest:
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.user.is_authenticated:
        article_id = request.POST['article_id']
        article = get_article(article_id)

        add_like(article, request.user)
        data = {
            'is_liked': True,
            'total_likes': get_fans(article).count()
        }
        return JsonResponse(data)
    else:
        return HttpResponseBadRequest('Invalid request')


# Удаления лайка со статьи
@require_POST
def remove_like_article(request) -> JsonResponse | HttpResponseBadRequest:
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.user.is_authenticated:
        article_id = request.POST['article_id']
        article = get_article(article_id)
        remove_like(article, request.user)
        data = {
            'is_liked': False,
            'total_likes': get_fans(article).count()
        }
        return JsonResponse(data)
    else:
        return HttpResponseBadRequest('Invalid request')


# Добавления лайка для комментария
@require_POST
def add_like_comment(request) -> JsonResponse | HttpResponseBadRequest:
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax and request.user.is_authenticated:
        comment_id = request.POST['comment_id']
        comment = get_comment(comment_id)
        add_like(comment, request.user)
        data = {
            'is_liked': True,
            'total_likes': get_fans(comment).count()
        }

        return JsonResponse(data)
    else:
        return HttpResponseBadRequest('Invalid request')


# Удаления лайка с комментария
@require_POST
def remove_like_comment(request) -> JsonResponse | HttpResponseBadRequest:
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax and request.user.is_authenticated:
        comment_id = request.POST['comment_id']
        comment = get_comment(comment_id)
        remove_like(comment, request.user)
        data = {
            'is_liked': False,
            'total_likes': get_fans(comment).count()
        }
        return JsonResponse(data)
    else:
        return HttpResponseBadRequest('Invalid request')
