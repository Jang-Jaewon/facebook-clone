from django.contrib import admin
from . import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "nickname", "user", "picture"]
    list_display_links = ["nickname", "user"]
    search_fields = ["nickname"]


@admin.register(models.Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ["current_user", "user", "created_at"]
    list_display_links = ["current_user", "user"]


@admin.register(models.FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ["id", "from_user", "to_user", "created_at"]
    list_display_links = ["from_user", "to_user", "created_at"]
