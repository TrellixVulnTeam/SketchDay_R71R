from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from diary.models import Diary

# Create your views here.

class IndexView(ListView):
    model = Diary
    template_name = 'diary/diary.html'
    context_object_name = 'diarys'
    # paginate_by = 8
    ordering = ['-dt_created']
