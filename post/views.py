from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import get_user_model
from .models import *
from .forms import CommentForm, PostForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
from django.contrib import messages
from django.db.models import Count  # ๐ 'Count' import
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.
def post_list(request, tag=None):  # ๐ tag๊ฐ url์ ํตํด ์ ๋ฌ๋์ง ์์๋๋ None๊ฐ ํ ๋น
    tag_all = Tag.objects.annotate(num_post=Count("post")).order_by(
        "-num_post"
    )  # ๐ ๋ชจ๋  ํ๊ทธ๋ฅผ ์ ๋ ฌํ์ฌ ๊ฐ์ ธ์ต๋๋ค.
    if tag:
        post_list = Post.objects.filter(
            tag_set__name__iexact=tag
        )  # ๐ Tag์ ์ด๋ฆ๊ณผ ์ ํํ ์ผ์นํ๋ Post๋ฅผ ๊ฐ์ ธ์ต๋๋ค
    else:
        post_list = Post.objects.all()  # ๐ argument๋ก ๋ค์ด์จ tag๊ฐ ์๋ค๋ฉด, ๋ชจ๋๋ฅผ ์ถ๋ ฅ
    if request.method == "POST":
        tag = request.POST.get("tag")
        tag_clean = "".join(e for e in tag if e.isalnum())  # ๐ ์ซ์๋ ๋ฌธ์์ด๋ก ๋ค์ด์์ ๋, ์๋
        return redirect("post:post_search", tag_clean)

    comment_form = CommentForm()

    # Paginaion
    paginator = Paginator(post_list, 3)
    page_num = request.POST.get("page")
    try:
        posts = paginator.page(page_num)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    if request.is_ajax():
        return render(
            request,
            "post/post_list_ajax.html",
            {
                "posts": posts,
                "comment_form": comment_form,
            },
        )

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


@login_required  # ๐ login์ด ๋ ์ํ์์๋ง ์๋ ํจ์๋ฅผ ์๋์์ผ์:)
@require_POST  # ๐ POST ๋ฐฉ์์ผ๋ก๋ง ๊ฐ์ ๋ฐ์ ์ ์์ด์:)
def post_like(request):
    pk = request.POST.get("pk", None)  # ๐ ๊ฒ์๊ธ์ pk๊ฐ์ ๊ฐ์ ธ์ต๋๋ค.
    post = get_object_or_404(Post, pk=pk)  # ๐ pk๊ฐ์ผ๋ก ๊ฒ์๊ธ์ Object๋ฅผ ๊ฐ์ ธ์ต๋๋ค.
    post_like, post_like_created = post.like_set.get_or_create(user=request.user)

    if not post_like_created:  # ๐ ์์ฑ๋ ์ข์์๊ฐ ์ด๋ฏธ ์๋ค๋ฉด,
        post_like.delete()  # ๐ post_like ์ญ์ 
        message = "์ข์์ ์ทจ์"
    else:  # ๐ ์์ฑ๋ ์ข์์๊ฐ ์์ด์ ์์ฑ๋์๋ค๋ฉด,
        message = "์ข์์"

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

    if not post_bookmark_created:  # ๐ ๋ถ๋งํฌ๊ฐ ๋์ด์๋ค๋ฉด,
        post_bookmark.delete()  # ๐ ๋ถ๋งํฌ Object ์ญ์ 
        message = "๋ถ๋งํฌ ์ทจ์"
        is_bookmarked = "N"  # ๐ is_bookmarked์ N์ ๋ด์
    else:
        message = "๋ถ๋งํฌ"
        is_bookmarked = "Y"  # ๐ is_bookmarked์ Y์ ๋ด์

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
            messages.info(request, "์ ๊ธ์ด ๋ฑ๋ก๋์์ต๋๋ค")
            return redirect("post:post_list")
    else:
        form = PostForm()
    return redirect("post:post_list")


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.warning(request, "์๋ชป๋ ์ ๊ทผ์๋๋ค")
        return redirect("post:post_list")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            post.tag_set.clear()
            post.tag_save()
            messages.success(request, "์์ ์๋ฃ")
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
        messages.warning(request, "์๋ชป๋ ์ ๊ทผ์๋๋ค")
        return redirect("post:post_list")

    if request.method == "POST":
        post.delete()
        return redirect("post:post_list")


@login_required
def comment_new(request):
    pk = request.POST.get("pk")  # ๐ pk๊ฐ
    post = get_object_or_404(Post, pk=pk)  # ๐ pk๊ฐ์ผ๋ก Post Object ๊ฐ์ ธ์ด
    if request.method == "POST":
        form = CommentForm(request.POST)  # ๐ form์ ์๋ ฅ ์ ๋ณด๋ฅผ CommentForm์ ์ ๋ฌ
        if form.is_valid():  # ๐ ์ ํจ์ฑ ๊ฒ์ฌ
            comment = form.save(commit=False)  # ๐ ์ ์ฅ ๊ฐ๋ก์ฑ๊ธฐ
            comment.author = request.user
            comment.post = post
            comment.save()  # ๐ Object ์ ์ฅ
            return render(
                request,
                "post/comment_new_ajax.html",
                {
                    "comment": comment,
                },
            )
    return redirect("post:post_list")  # ๐ post_list ๋ค์ ํธ์ถ


@login_required
def comment_delete(request):
    pk = request.POST.get("pk")  # ๐ pk๊ฐ
    comment = get_object_or_404(Comment, pk=pk)  # ๐ Comment Object ๊ฐ์ ธ์ด
    if request.method == "POST" and request.user == comment.author:
        comment.delete()
        message = "์ญ์ ์๋ฃ"
        status = 1
    else:
        message = "์๋ชป๋ ์ ๊ทผ์๋๋ค"
        status = 0

    return HttpResponse(
        json.dumps({"message": message, "status": status}),
        content_type="application/json",
    )
