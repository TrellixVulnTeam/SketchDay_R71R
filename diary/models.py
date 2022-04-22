from xmlrpc.client import Boolean
from django.db import models
from Login.models import User
# Create your models here.
class Diary(models.Model):
    
    title = models.CharField(max_length=60)
    content = models.TextField()
    dt_created = models.DateField()
    public_TF = models.BooleanField(default=True)
    comment_TF = models.BooleanField(default=True)
    image = models.ImageField(blank=True, upload_to ='item_pics')
    emotion = models.CharField(max_length=10)
    
    # User 모델 접근
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # 관리자 페이지에서 title로 보이게 하기 위해
    def __str__(self):
        return self.title


