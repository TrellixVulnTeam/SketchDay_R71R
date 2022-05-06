from django.shortcuts import redirect, render
from allauth.account.views import PasswordChangeView
from django.urls import reverse
from calendar import HTMLCalendar
from django.views.generic import DetailView, UpdateView
from matplotlib.style import context
from diary.models import Diary
from Login.models import User
from .forms import ProfileForm
from braces.views import LoginRequiredMixin
# Create your views here

def index(request):
    return redirect('account_login')


# 비밀번호 변경
class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    def get_success_url(self):
        return reverse('profile', kwargs={'user_id': self.request.user.id})
    
# 프로필 페이지   
class ProfileView(DetailView):
    model = User
    template_name = "Login/profile.html"
    pk_url_kwarg = 'user_id'
    context_object_name = "profile_user"

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        if user_id == self.request.user:
            context['user_diary'] =  Diary.objects.filter(author__id = user_id).order_by("-dt_created")[:4]
        else:
            context['user_diary'] =  Diary.objects.filter(public_TF=True, author__id = user_id).order_by('-dt_created')[:4]
        return context


# 프로필 설정
class ProfileSetView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'Login/profile_set_form.html'
    
    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('cal:calendar')

# 프로필 수정
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'Login/profile_update_form.html'


    def get_object(self, queryset=None):
        return self.request.user
    
    def get_success_url(self):
        return reverse('profile', kwargs={'user_id': self.request.user.id})
