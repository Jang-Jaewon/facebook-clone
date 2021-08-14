from django.contrib import admin
from .models import *


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "author", "nickname", "content", "created_at"]
    list_display_links = ["author", "nickname", "content"]

    def nickname(request, post):
        # print(post) # Post object (1)
        return post.author.profile.nickname
