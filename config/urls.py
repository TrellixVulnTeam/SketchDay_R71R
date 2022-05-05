"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path ,include
from Login.views import CustomPasswordChangeView
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    #admin
    path('admin/', admin.site.urls),

    #calendar
    path('calendar/', include('emotion_calendar.urls')),
    
    #Diary
    path('diary/', include('diary.urls')),
    
    #Login
    path('', include('Login.urls')),
    
    # 이메일 재인증
    path(
        'email-confirmation-required/',
        TemplateView.as_view(template_name='account/email_confirmation_required.html'),
        name='account_email_confirmation_required',
    ),
    # 이메일 변경
    path(
        'email-confirmation-done/',
        TemplateView.as_view(template_name='account/email_confirmation_done.html'),
        name='account_email_confirmation_done',
    ),
    # 비밀번호 변경
    path(
        'password/change/',
        CustomPasswordChangeView.as_view(),
        name ="account_change_password",
        ),
    path('', include('allauth.urls')),

]
# 개발 모드에서만 디버그, 배포에서는 동작 안함
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns += [
    path('__debug__/', include(debug_toolbar.urls)),
    ]