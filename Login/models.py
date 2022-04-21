from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    #닉네임 필드 추가
    nickname = models.CharField(
        max_length=15, 
        unique=True,
        null=True,
        error_messages={'unique' : "이미 사용중인 닉네임 입니다."}
        )
    
    # 기본값을 username 에서 email로 변환
    def __str__(self):
        return self.email