# Generated by Django 3.2.9 on 2023-01-05 15:53

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_article_last_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_text',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Текст'),
        ),
    ]
