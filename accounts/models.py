from django.db import models
from django.conf import settings  # π settgins.py
from imagekit.models import ProcessedImageField  # π μ΄λ―Έμ§ μ²λ¦¬
from imagekit.processors import ResizeToFill  # π μ¬μ΄μ¦ λ³κ²½
import re  # π μ κ·ννμ


def user_path(instance, filename):
    from random import choice
    import string

    arr = [
        choice(string.ascii_letters) for _ in range(8)
    ]  # π ascii codeλ₯Ό ν¬ν¨νμ¬ 8κ°μ μμλ₯Ό κ°μ§ list μμ±
    pid = "".join(arr)  # π srtingμΌλ‘ ν©μΉ¨
    extension = filename.split(".")[-1]  # π νμ₯μ(νμΌμ΄λ¦μ .μ κΈ°μ€μΌλ‘ λ§μ§λ§ μμ κ°μ Έμ΄)
    return "accounts/picture/{}/{}.{}".format(instance.user.username, pid, extension)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(
        "λ³λͺ", max_length=30, unique=True
    )  # π CharFieldλ max_lengthκ° νμκ°μ
    picture = ProcessedImageField(
        upload_to=user_path,  # π μ μ₯λλ κ²½λ‘
        processors=[ResizeToFill(150, 150)],  # π μ¬μ΄μ¦ μ‘°μ 
        format="JPEG",  # π format
        options={"quality": 90},
        blank=True,
    )

    about = models.CharField(max_length=300, blank=True)

    GENDER_C = (
        ("μ νμν¨", "μ νμν¨"),
        ("μ¬μ±", "μ¬μ±"),
        ("λ¨μ±", "λ¨μ±"),
    )

    gender = models.CharField("μ±λ³(μ νμ¬ν­)", max_length=10, choices=GENDER_C, default="N")


class Friend(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, on_delete=models.CASCADE
    )
    # room = ForeignKey(Room, blank=True, on_delete=models.SET_NULL, null=True) # μ±ν κ΄λ ¨ field
    current_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="friends",
        blank=True,
        on_delete=models.CASCADE,
    )
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class FriendRequest(models.Model):
    # μμ²­νλ μ¬λ
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="friend_requests",
        on_delete=models.CASCADE,
    )
    # μμ²­λ°λ μ¬λ
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="requested_friend_requests",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} => {}".format(self.from_user, self.to_user)

    class Meta:
        unique_together = ("from_user", "to_user")
