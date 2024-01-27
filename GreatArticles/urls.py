"""GreatArticles URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the includes() function: from django.urls import includes, path
    2. Add a URL to urlpatterns:  path('blog/', includes('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.views.generic import TemplateView

from GreatArticles.sitemaps import ArticleSitemap
from GreatArticles.views import terms, privacy

sitemaps = {
    'article': ArticleSitemap
}

urlpatterns = [
                  path('terms/', terms, name='terms'),
                  path('privacy/', privacy, name='privacy'),
                  path('admin/', admin.site.urls),
                  path('likes/', include('likes.urls')),  # Лайки
                  path('profile/', include('userprofile.urls')),  # Профиль
                  path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Выход из аккаунта
                  path("ckeditor5/", include('django_ckeditor_5.urls')),  # Редактор
                  path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
                  path('robots.txt/', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
                  path('auth/', include('social_django.urls', namespace='social')),

                  path('', include('articles.urls')),  # Главная страница
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)

handler404 = "GreatArticles.views.page_not_found"
