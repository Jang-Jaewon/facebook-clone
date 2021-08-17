from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from .models import *
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json

# Create your views here.
def post_list(request):
    post_list = Post.objects.all()

    if request.user.is_authenticated:
        username = request.user
        user = get_object_or_404(get_user_model(), username=username)
        # print(user.profile)
        user_profile = user.profile
        return render(
            request,
            "post/post_list.html",
            {"user_profile": user_profile, "posts": post_list},
        )
    else:
        return render(
            request,
            "post/post_list.html",
            {"posts": post_list},
        )


@login_required  # 👈 login이 된 상태에서만 아래 함수를 작동시켜요:)
@require_POST  # 👈 POST 방식으로만 값을 받을 수 있어요:)
def post_like(request):
    pk = request.POST.get("pk", None)  # 👈 게시글의 pk값을 가져옵니다.
    post = get_object_or_404(Post, pk=pk)  # 👈 pk값으로 게시글의 Object를 가져옵니다.
    post_like, post_like_created = post.like_set.get_or_create(user=request.user)

    if not post_like_created:  # 👈 생성된 좋아요가 이미 있다면,
        post_like.delete()  # 👈 post_like 삭제
        message = "좋아요 취소"
    else:  # 👈 생성된 좋아요가 없어서 생성되었다면,
        message = "좋아요"

    context = {"like_count": post.like_count, "message": message}

    return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
@require_POST
def post_bookmark(request):
    pk = request.POST.get("pk", None)
    post = get_object_or_404(Post, pk=pk)
    post_bookmark, post_bookmark_created = post.bookmark_set.get_or_create(
        user=request.user
    )

    if not post_bookmark_created:  # 👈 북마크가 되어있다면,
        post_bookmark.delete()  # 👈 북마크 Object 삭제
        message = "북마크 취소"
        is_bookmarked = "N"  # 👈 is_bookmarked에 N을 담음
    else:
        message = "북마크"
        is_bookmarked = "Y"  # 👈 is_bookmarked에 Y을 담음

    context = {"is_bookmarked": is_bookmarked, "message": message}

    return HttpResponse(json.dumps(context), content_type="application/json")
