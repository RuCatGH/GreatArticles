import os.path

from django.http import FileResponse, Http404
from django.shortcuts import render

from GreatArticles.settings import BASE_DIR
from articles.services import get_popular_articles


def page_not_found(request, exception):
    popular = get_popular_articles()
    return render(request, '404.html', {'popular': popular}, status=404)


def terms(request):
    try:
        return FileResponse(open(os.path.join(BASE_DIR, 'templates/terms.pdf'), 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()


def privacy(request):
    try:
        return FileResponse(open(os.path.join(BASE_DIR, 'templates/privacy.pdf'), 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()
