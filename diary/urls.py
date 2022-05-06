from django.urls import path
from . import views

urlpatterns = [
    # 전체 일기
    path('', views.MainView.as_view(), name='main'),
    
    #내 일기 전체보기
    path('users/<int:user_id>/diarys/', 
        views.UserDiaryListView.as_view(), 
        name='user-review-list'),
    

    path('detail/<int:diary_id>/', 
        views.diaryDetailView, 
        name='diary-detail'),
    
    path('new/<str:dt_selected>', 
        views.diaryCreateView, 
        name='diary-create_selected'),

    path('new/', 
        views.diaryCreateView, 
        name='diary-create'),
    
    #일기 수정
    path('<int:diary_id>/edit/', 
        views.diaryUpdateView, 
        name='diary-update'),
    
    #일기 삭제
    path('<int:diary_id>/delete/', 
        views.DiaryDeleteView.as_view(), 
        name='diary-delete'),
    
    # 노래 평가
    path('rating/', views.rating, name='music-rating'),

    # 댓글 추가
    path('<int:pk>/comment/write/', views.comment_write_view, name='comment-write'),
    # 댓글 삭제
    path('<int:pk>/commnet/delete/', views.comment_delete_view, name='comment-delete')
]
