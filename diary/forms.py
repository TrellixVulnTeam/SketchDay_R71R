from django import forms
from .models import Diary 
from django.forms.widgets import NumberInput

class DiaryCreateForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = [
            'title', 
            'content', 
            'public_TF',
            'comment_TF',
            'dt_created',
            ]
        
        widgets ={
            'public_TF': forms.RadioSelect(),
            'comment_TF' : forms.RadioSelect(),
            'dt_created' : forms.NumberInput(attrs={'type':'date'})
        }