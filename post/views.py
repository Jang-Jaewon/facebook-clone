from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import get_user_model
from .models import *
from .forms import CommentForm, PostForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
from django.contrib import messages
from django.db.models import Count  # 👈 'Count' import

# Create your views here.
def post_list(request, tag=None):  # 👈 tag가 url을 통해 전달되지 않을때는 None값 할당
    tag_all = Tag.objects.annotate(num_post=Count("post")).order_by(
        "-num_post"
    )  # 👈 모든 태그를 정렬하여 가져옵니다.
    if tag:
        post_list = Post.objects.filter(
            tag_set__name__iexact=tag
        )  # 👈 Tag의 이름과 정확히 일치하는 Post를 가져옵니다
    else:
        post_list = Post.objects.all()  # 👈 argument로 들어온 tag가 없다면, 모두를 출력
    if request.method == "POST":
        tag = request.POST.get("tag")
        tag_clean = "".join(e for e in tag if e.isalnum())  # 👈 숫자나 문자열로 들어왔을 때, 작동
        return redirect("post:post_search", tag_clean)

    # post_list = Post.objects.all() # 👈 삭제
    comment_form = CommentForm()

    if request.user.is_authenticated:
        username = request.user
        friends = username.friends.all()
        request_friends = username.friend_requests
        user = get_object_or_404(get_user_model(), username=username)
        user_profile = user.profile
        friend_list = user.friends.all()
        my_friend_user_list = list(map(lambda friend: friend.user, friend_list))
        friend_request_list = user.friend_requests.all()
        my_friend_request_user_list = list(
            map(lambda friend_request: friend_request.to_user, friend_request_list)
        )
        return render(
            request,
            "post/post_list.html",
            {
                "tag": tag,
                "tag_all": tag_all,
                "user_profile": user_profile,
                "posts": post_list,
                "friends": friends,
                "request_friends": request_friends,
                "my_friend_user_list": my_friend_user_list,
                "my_friend_request_user_list": my_friend_request_user_list,
                "comment_form": comment_form,
            },
        )
    else:
        return render(
            request,
            "post/post_list.html",
            {
                "tag": tag,
                "tag_all": tag_all,
                "posts": post_list,
                "comment_form": comment_form,
            },
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


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            post.tag_save()
            messages.info(request, "새 글이 등록되었습니다")
            return redirect("post:post_list")
    else:
        form = PostForm()
    return redirect("post:post_list")


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.warning(request, "잘못된 접근입니다")
        return redirect("post:post_list")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            post.tag_set.clear()
            post.tag_save()
            messages.success(request, "수정완료")
            return redirect("post:post_list")
    else:
        form = PostForm(instance=post)
    return render(
        request,
        "post/post_edit.html",
        {
            "post": post,
            "form": form,
        },
    )


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user or request.method == "GET":
        messages.warning(request, "잘못된 접근입니다")
        return redirect("post:post_list")

    if request.method == "POST":
        post.delete()
        return redirect("post:post_list")


@login_required
def comment_new(request):
    pk = request.POST.get("pk")  # 👈 pk값
    post = get_object_or_404(Post, pk=pk)  # 👈 pk값으로 Post Object 가져옴
    if request.method == "POST":
        form = CommentForm(request.POST)  # 👈 form의 입력 정보를 CommentForm에 전달
        if form.is_valid():  # 👈 유효성 검사
            comment = form.save(commit=False)  # 👈 저장 가로채기
            comment.author = request.user
            comment.post = post
            comment.save()  # 👈 Object 저장
            return render(
                request,
                "post/comment_new_ajax.html",
                {
                    "comment": comment,
                },
            )
    return redirect("post:post_list")  # 👈 post_list 다시 호출


@login_required
def comment_delete(request):
    pk = request.POST.get("pk")  # 👈 pk값
    comment = get_object_or_404(Comment, pk=pk)  # 👈 Comment Object 가져옴
    if request.method == "POST" and request.user == comment.author:
        comment.delete()
        message = "삭제완료"
        status = 1
    else:
        message = "잘못된 접근입니다"
        status = 0

    return HttpResponse(
        json.dumps({"message": message, "status": status}),
        content_type="application/json",
    )
