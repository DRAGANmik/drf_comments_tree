from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Article, Comment


class ArticleAdmin(admin.ModelAdmin):
    pass


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, MPTTModelAdmin)
