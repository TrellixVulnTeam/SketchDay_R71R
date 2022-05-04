from django.contrib import admin
from diary.models import Diary, Comment

# Register your models here.
admin.site.register(Diary)
admin.site.register(Comment)