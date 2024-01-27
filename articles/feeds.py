from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse

from articles.models import Article


class LatestPostsFeed(Feed):
    title = "GreatArticles"
    link = "https://greatarticles.ru"
    description = "На нашем сайте появилась новая статья!"

    def items(self):
        return Article.objects.filter(is_published=True).order_by('-pub_date')[:10]

    def item_title(self, item):
        return item.article_title

    def item_description(self, item):
        return truncatewords(item.article_text, 30)

    def item_link(self, item):
        return reverse('articles:detail', args=[item.slug])

    def item_enclosure_url(self, item):
        return item.article_image.url


