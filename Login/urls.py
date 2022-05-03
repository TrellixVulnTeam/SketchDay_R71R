from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    
    #프로필 링크
    path('users/<int:user_id>', 
        views.ProfileView.as_view(), 
        name='profile'),
    
    #프로필 설정
    path('set-profile/', 
        views.ProfileSetView.as_view(), 
        name='profile-set'),
    
    #프로필 수정
    path('edit-profile/', 
        views.ProfileUpdateView.as_view(), 
        name='profile-update'),

]