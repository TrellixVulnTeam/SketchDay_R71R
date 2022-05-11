from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_no_special_characters
# Create your models here.

class User(AbstractUser):
    #닉네임 필드 추가
    nickname = models.CharField(
        max_length=15, 
        unique=True,
        null=True,
        validators = [validate_no_special_characters],
        error_messages={'unique' : "이미 사용중인 닉네임 입니다."}
    )
    
    profile_pic = models.ImageField(default = "default_profile_pic.jpg", upload_to='profile_pics') 
    
    # 기본값을 username 에서 email로 변환
    def __str__(self):
        return self.email

