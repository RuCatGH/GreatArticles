from django.contrib import admin

from .models import Article, Comment, Ip, Category


class NewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('article_title',)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Article, NewsAdmin)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(Ip)
