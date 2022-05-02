# 접근제어를 위한 미들웨어
from django.urls import reverse
from django.shortcuts import redirect

class ProfileSetupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # request
        # 유저가 로그인이 돼있고, 
        # 프로필을 설정하지 않았고, 
        # 프로필 설정 페이지가 아닌 다른 페이지로 들어가려고 하면
        if (
            request.user.is_authenticated and
            not request.user.nickname and
            request.path_info != reverse('profile-set')
        ):
            return redirect('profile-set')

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response