from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE  # 👈 settgins.py
from imagekit.models import ProcessedImageField  # 👈 이미지 처리
from imagekit.processors import ResizeToFill  # 👈 사이즈 변경
import re  # 👈 정규표현식


def user_path(instance, filename):
    from random import choice
    import string

    arr = [
        choice(string.ascii_letters) for _ in range(8)
    ]  # 👈 ascii code를 포함하여 8개의 원소를 가진 list 생성
    pid = "".join(arr)  # 👈 srting으로 합침
    extension = filename.split(".")[-1]  # 👈 확장자(파일이름을 .을 기준으로 마지막 요소 가져옴)
    return "accounts/picture/{}/{}.{}".format(instance.user.username, pid, extension)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(
        "별명", max_length=30, unique=True
    )  # 👈 CharField는 max_length가 필수값임
    picture = ProcessedImageField(
        upload_to=user_path,  # 👈 저장되는 경로
        processors=[ResizeToFill(150, 150)],  # 👈 사이즈 조절
        format="JPEG",  # 👈 format
        options={"quality": 90},
        blank=True,
    )

    about = models.CharField(max_length=300, blank=True)

    GENDER_C = (
        ("선택안함", "선택안함"),
        ("여성", "여성"),
        ("남성", "남성"),
    )

    gender = models.CharField("성별(선택사항)", max_length=10, choices=GENDER_C, default="N")
