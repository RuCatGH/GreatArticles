# Generated by Django 3.2.9 on 2022-12-07 20:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import gradient_colorfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_title', models.CharField(max_length=200, verbose_name='Название статьи')),
                ('header_background', gradient_colorfield.fields.GradientColorField(default='linear-gradient(to bottom, #fff 0%, #fff 100%)', max_length=100, null=True, verbose_name='Header Background')),
                ('article_text', models.TextField(verbose_name='Текст статьи')),
                ('min_text', models.CharField(max_length=300, verbose_name='Мин текст')),
                ('pub_date', models.DateField(verbose_name='Дата публикации')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='URL')),
                ('article_image', models.ImageField(blank=True, null=True, upload_to='img/', verbose_name='Изображение')),
                ('article_author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('slug', models.SlugField(max_length=200, null=True, unique=True, verbose_name='URL')),
            ],
        ),
        migrations.CreateModel(
            name='Ip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField(verbose_name='Текст комментария')),
                ('comment_date', models.DateField(auto_now=True, verbose_name='date')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.article')),
                ('comment_author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария')),
                ('reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='articles.comment')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='articles.category'),
        ),
        migrations.AddField(
            model_name='article',
            name='views',
            field=models.ManyToManyField(blank=True, related_name='post_views', to='articles.Ip'),
        ),
    ]