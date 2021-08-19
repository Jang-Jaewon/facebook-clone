from django import forms
from .models import Comment, Post


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"size": "70px", "placeholder": "댓글 달기...", "maxlength": "40"}
        ),
    )

    class Meta:
        model = Comment
        fields = ["content"]


class PostForm(forms.ModelForm):
    photo = forms.ImageField(label="", required=False)
    content = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "class": "post-new-content",
                "rows": 5,
                "cols": 50,
                "placeholder": "무슨 생각을 하시나요?(140자 가능)",
            }
        ),
    )

    class Meta:
        model = Post
        fields = ["photo", "content"]
