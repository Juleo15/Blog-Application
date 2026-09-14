from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "publish", "created_at")
    list_filter = ("status", "created_at", "author")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}