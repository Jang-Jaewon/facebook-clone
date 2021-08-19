from django.contrib import admin
from .models import *


class LikeInline(admin.TabularInline):
    model = Like


class CommentInline(admin.TabularInline):
    model = Comment


class BookmarkInline(admin.TabularInline):
    model = Bookmark


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "author", "nickname", "content", "created_at"]
    list_display_links = ["author", "nickname", "content"]
    inlines = [LikeInline, CommentInline, BookmarkInline]

    def nickname(request, post):
        # print(post) # Post object (1)
        return post.author.profile.nickname


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ["id", "post", "user", "created_at"]
    list_display_links = ["post", "user"]


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ["id", "post", "user", "created_at"]
    list_display_links = ["post", "user"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["post", "content", "author", "created_at"]
    list_display_links = ["post", "content", "author"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name"]
