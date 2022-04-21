from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User , UserAdmin)
UserAdmin.fieldsets += (("Custom fields", {"fields": ("nickname",)}),)
# 추가된 닉네임 필드는 어드민 페이지에 추가되지 않기 때문에 따로 추가