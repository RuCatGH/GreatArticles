import uuid

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field

from articles.fields import WEBPField
from gradient_colorfield.fields import GradientColorField
from likes.models import Like
from userprofile.models import CustomUser


def image_folder(instance, filename):
    return 'articles/img/{}.webp'.format(uuid.uuid4().hex)


class Article(models.Model):
    # Описание модели по статьям.
    article_author = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    article_title = models.CharField('Название статьи', max_length=200)
    description = models.CharField('Описание статьи', max_length=500, default=None, blank=False)
    header_background = GradientColorField(verbose_name=u'Header Background',
                                           default='linear-gradient(to bottom, #fff 0%, #fff 100%)',
                                           null=True
                                           )
    article_text = CKEditor5Field('Текст', config_name='extends')
    pub_date = models.DateField('Дата публикации')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL")
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)

    article_image = WEBPField(
        verbose_name='Image',
        upload_to=image_folder,
    )
    views = models.ManyToManyField('Ip', related_name="post_views", blank=True)
    likes = GenericRelation(Like)
    last_modified = models.DateTimeField(auto_now=True)
    keywords = models.CharField('Ключи', max_length=255, blank=True, default='')

    is_published = models.BooleanField(default=True)

    def total_views(self):
        # Метод возращающий общее количество просмотров поста.
        return self.views.count()

    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.article_title or ''

    def get_absolute_url(self):
        return reverse('articles:detail', kwargs={'slug': self.slug})


class Ip(models.Model):
    # Айпи пользователя
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True, verbose_name="URL", null=True)
    keywords = models.CharField('Ключи', max_length=255, blank=True, default='')
    description = models.CharField('Описание категории', max_length=250, default='', blank=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    # Описние модели по комментариям.
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comment')
    comment_author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Автор комментария',
                                       null=True)
    comment_text = models.TextField('Текст комментария')
    comment_date = models.DateField(u'date', auto_now=True)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    likes = GenericRelation(Like)

    @property
    def total_likes(self):
        return self.likes.count()
