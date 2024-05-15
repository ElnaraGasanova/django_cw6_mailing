from django.contrib import admin
from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'content', 'published_date', 'views_count',)
    list_filter = ('title', 'published_date',)
    search_fields = ('title', 'content',)
