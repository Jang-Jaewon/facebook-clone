from django import forms
from django.contrib.auth import get_user_model  # π Djangoμ μ¬μ©μ Model Object νΈμΆ
from django.contrib.auth.forms import UserCreationForm  # π λ΄μ₯λ νμκ°μ form
from .models import Profile
from django.contrib.auth.models import User  # π λ΄μ₯λ User Model


class LoginForm(forms.ModelForm):  # π ModelForm μμ
    class Meta:
        model = User
        fields = ["username", "password"]


class SignupForm(UserCreationForm):  # π μ΄λ―Έ μ‘΄μ¬νλ νμκ°μ Form μμ
    username = forms.CharField(
        label="μ¬μ©μλͺ",
        widget=forms.TextInput(
            attrs={"pattern": "[a-zA-Z0-9]+", "title": "νΉμλ¬Έμ, κ³΅λ°± μλ ₯ λΆκ°"}
        ),
    )
    nickname = forms.CharField(label="λλ€μ")
    picture = forms.ImageField(label="νλ‘ν μ¬μ§", required=False)

    class Meta(UserCreationForm.Meta):  # π
        fields = UserCreationForm.Meta.fields + ("email",)

    def clean_nickname(self):
        nickname = self.cleaned_data.get("nickname")
        if Profile.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError("μ΄λ―Έ μ‘΄μ¬νλ λλ€μ μλλ€.")
        return nickname

    def clean_email(self):
        email = self.cleaned_data.get("email")
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("μ΄λ―Έ μ¬μ©μ€μΈ μ΄λ©μΌ μλλ€.")
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
