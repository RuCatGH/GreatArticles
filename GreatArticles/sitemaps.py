from django.contrib.sitemaps import Sitemap
from django.contrib.sites.models import Site

from articles.models import Article


class ArticleSitemap(Sitemap):
    location = ""

    def get_urls(self, site=None, **kwargs):
        site = Site(domain='greatarticles.ru', name='greatarticles.ru')
        return super(ArticleSitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.last_modified

    def location(self, obj):
        return "/{}/".format(obj.slug)
