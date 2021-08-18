from django.urls import path
from . import views

app_name = "post"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("like", views.post_like, name="post_like"),
    path("bookmark", views.post_bookmark, name="post_bookmark"),
    path("comment/new", views.comment_new, name="comment_new"),
    path("comment/delete", views.comment_delete, name="comment_delete"),
]
