# Generated by Django 4.1.5 on 2023-07-02 08:36

import articles.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0020_alter_article_is_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_image',
            field=articles.fields.WEBPField(height_field='637', upload_to='articles/img', verbose_name='Image', width_field='837'),
        ),
    ]