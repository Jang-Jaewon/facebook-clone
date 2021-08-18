from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth import logout as django_logout
from .forms import SignupForm, LoginForm
from django.http import HttpResponse
import json


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return redirect("accounts:login")
    else:
        form = SignupForm()

    return render(
        request,
        "accounts/signup.html",
        {
            "form": form,
        },
    )


def login_check(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        name = request.POST.get("username")
        pwd = request.POST.get("password")
        user = authenticate(username=name, password=pwd)
        if user is not None:
            login(request, user)
            return redirect("/")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", context={"form": form})


def logout(request):
    django_logout(request)
    return redirect("/")


def create_friend_request(request):
    user_id = request.POST.get("pk", None)  # 👈 POST방식으로 받아온 추가할 사용자의 pk값
    user = request.user  # 👈 요청을 보낸 사용자의 정보
    target_user = get_object_or_404(
        get_user_model(), pk=user_id
    )  # 👈 요청을 받을 사용자의 Object
    try:
        user.friend_requests.create(
            from_user=user, to_user=target_user
        )  # related_name 접근
        context = {"result": "succes"}
    except Exception as ex:
        print("에러가 발생했습니다", ex)
        context = {
            "result": "error",
        }
    return HttpResponse(json.dumps(context), content_type="application/json")


def accept_friend_request(request):
    friend_request_id = request.POST.get("pk", None)  # 👈 요청에 대한 pk
    friend_request = FriendRequest.objects.get(
        pk=friend_request_id
    )  # 👈 FriendRequest에서 Object 가져옴
    from_user = friend_request.from_user  # 👈 요청한 사용자
    to_user = friend_request.to_user  # 👈 요청받은 사용자

    try:
        # 친구관계 생성
        # room_name= "{},{}".format(from_user.username, to_user.username)

        # 채팅방을 만들고
        # room = Room.objects.create(room_name=room_name)
        # Friend.objects.create(user=from_user, current_user=to_user, room=room)
        # Friend.objects.create(user=to_user, current_user=from_user, room=room)
        Friend.objects.create(user=from_user, current_user=to_user)
        Friend.objects.create(user=to_user, current_user=from_user)
        friend_request.delete()  # 👈 현재 만들어진 친구요청을 삭제
        context = {
            "result": "success",
        }
    except Exception as ex:
        print("에러가 발생했습니다", ex)
        context = {
            "result": "error",
        }
    return HttpResponse(json.dumps(context), content_type="application/json")
