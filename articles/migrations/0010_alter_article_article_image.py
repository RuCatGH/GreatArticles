# Generated by Django 3.2.9 on 2023-01-08 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0009_alter_article_article_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_image',
            field=models.ImageField(blank=True, null=True, upload_to='articles/img', verbose_name='Изображение'),
        ),
    ]