from django import forms
from .models import User

# 회원가입 폼
class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["nickname"]
        
    #데이터를 유저 인스턴스에 저장해 줍니다.
    def signup(self,request,user):
        user.nickname = self.cleaned_data["nickname"]
        user.save()