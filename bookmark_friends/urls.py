from django.urls import path
from . import views

app_name = "bookmark_friends"
urlpatterns = [
    path("", views.bookmark_friends_list, name="bookmark_friends_list"),
]
