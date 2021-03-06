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
    user_id = request.POST.get("pk", None)  # π POSTλ°©μμΌλ‘ λ°μμ¨ μΆκ°ν  μ¬μ©μμ pkκ°
    user = request.user  # π μμ²­μ λ³΄λΈ μ¬μ©μμ μ λ³΄
    target_user = get_object_or_404(
        get_user_model(), pk=user_id
    )  # π μμ²­μ λ°μ μ¬μ©μμ Object
    try:
        user.friend_requests.create(
            from_user=user, to_user=target_user
        )  # related_name μ κ·Ό
        context = {"result": "succes"}
    except Exception as ex:
        print("μλ¬κ° λ°μνμ΅λλ€", ex)
        context = {
            "result": "error",
        }
    return HttpResponse(json.dumps(context), content_type="application/json")


def accept_friend_request(request):
    friend_request_id = request.POST.get("pk", None)  # π μμ²­μ λν pk
    friend_request = FriendRequest.objects.get(
        pk=friend_request_id
    )  # π FriendRequestμμ Object κ°μ Έμ΄
    from_user = friend_request.from_user  # π μμ²­ν μ¬μ©μ
    to_user = friend_request.to_user  # π μμ²­λ°μ μ¬μ©μ

    try:
        # μΉκ΅¬κ΄κ³ μμ±
        # room_name= "{},{}".format(from_user.username, to_user.username)

        # μ±νλ°©μ λ§λ€κ³ 
        # room = Room.objects.create(room_name=room_name)
        # Friend.objects.create(user=from_user, current_user=to_user, room=room)
        # Friend.objects.create(user=to_user, current_user=from_user, room=room)
        Friend.objects.create(user=from_user, current_user=to_user)
        Friend.objects.create(user=to_user, current_user=from_user)
        friend_request.delete()  # π νμ¬ λ§λ€μ΄μ§ μΉκ΅¬μμ²­μ μ­μ 
        context = {
            "result": "success",
        }
    except Exception as ex:
        print("μλ¬κ° λ°μνμ΅λλ€", ex)
        context = {
            "result": "error",
        }
    return HttpResponse(json.dumps(context), content_type="application/json")
