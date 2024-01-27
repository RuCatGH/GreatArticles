# Generated by Django 4.1.5 on 2023-07-02 08:37

import articles.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0021_alter_article_article_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_image',
            field=articles.fields.WEBPField(height_field='height', upload_to='articles/img', verbose_name='Image', width_field='width'),
        ),
    ]