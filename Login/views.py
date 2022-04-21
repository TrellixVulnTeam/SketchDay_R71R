from django.shortcuts import render
from allauth.account.views import PasswordChangeView
from django.urls import reverse
from calendar import HTMLCalendar



# Create your views here

def index(request):
    return render(request, 'Login/index.html')


class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        return reverse("index")