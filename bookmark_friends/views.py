from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from post.models import *


def bookmark_friends_list(request):
    username = request.user
    user = get_object_or_404(get_user_model(), username=username)
    user_profile = user.profile
    post_list = Post.objects.all()
    context = {
        "user_profile": user_profile,
        "post_list": post_list,
    }
    return render(
        request,
        "bookmark_friends/bookmark_friends_list.html",
        context,
    )
