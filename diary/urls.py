from django.urls import path
from . import views

urlpatterns = [
    # 전체 일기
    path('', views.MainView.as_view(), name='main'),
    # 내 일기
    path('me/', views.MyDiaryView.as_view(), name='my-diary'),
    
    #일기 내용
    # path('detail/<int:diary_id>/', 
    #     views.DiaryDetailView.as_view(), 
    #     name='diary-detail'),
    path('detail/<int:diary_id>/', 
        views.diaryDetailView, 
        name='diary-detail'),
    
    #일기작성
    # path('new/', 
    #     views.DiaryCreateView.as_view(), 
    #     name='diary-create'),
    path('new/<str:dt_selected>', 
        views.diaryCreateView, 
        name='diary-create_selected'),

    path('new/', 
        views.diaryCreateView, 
        name='diary-create'),
    
    #일기 수정
    path('<int:diary_id>/edit/', 
        views.DiaryUpdateView.as_view(), 
        name='diary-update'),
    
    #일기 삭제
    path('<int:diary_id>/delete/', 
        views.DiaryDeleteView.as_view(), 
        name='diary-delete'),
]
