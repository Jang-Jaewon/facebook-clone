from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_check, name="login"),
    path("logout/", views.logout, name="logout"),
    path(
        "create_friend_request/",
        views.create_friend_request,
        name="create_friend_request",
    ),
    path(
        "accept_friend_request/",
        views.accept_friend_request,
        name="accept_friend_request",
    ),
]
