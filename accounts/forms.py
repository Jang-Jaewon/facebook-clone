from django import forms
from django.contrib.auth import get_user_model  # 👈 Django의 사용자 Model Object 호출
from django.contrib.auth.forms import UserCreationForm  # 👈 내장된 회원가입 form
from .models import Profile
from django.contrib.auth.models import User  # 👈 내장된 User Model


class LoginForm(forms.ModelForm):  # 👈 ModelForm 상속
    class Meta:
        model = User
        fields = ["username", "password"]


class SignupForm(UserCreationForm):  # 👈 이미 존재하는 회원가입 Form 상속
    username = forms.CharField(
        label="사용자명",
        widget=forms.TextInput(
            attrs={"pattern": "[a-zA-Z0-9]+", "title": "특수문자, 공백 입력 불가"}
        ),
    )
    nickname = forms.CharField(label="닉네임")
    picture = forms.ImageField(label="프로필 사진", required=False)

    class Meta(UserCreationForm.Meta):  # 👈
        fields = UserCreationForm.Meta.fields + ("email",)

    def clean_nickname(self):
        nickname = self.cleaned_data.get("nickname")
        if Profile.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError("이미 존재하는 닉네임 입니다.")
        return nickname

    def clean_email(self):
        email = self.cleaned_data.get("email")
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("이미 사용중인 이메일 입니다.")
        return email

    def clean_picture(self):
        picture = self.cleaned_data.get("picture")
        if not picture:
            picture = None
        return picture

    def save(self):
        user = super().save()
        Profile.objects.create(
            user=user,
            nickname=self.cleaned_data["nickname"],
            picture=self.cleaned_data["picture"],
        )
        return user
