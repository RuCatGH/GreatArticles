# Generated by Django 4.1.5 on 2023-06-24 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0017_alter_article_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_enabled',
            field=models.BooleanField(default=False),
        ),
    ]
