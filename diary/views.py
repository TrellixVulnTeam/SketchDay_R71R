from django.shortcuts import render
from django.urls import reverse
# generic view
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from diary.models import Diary
from diary.forms import DiaryCreateForm


# Create your views here.

# main 화면 일단은 일기 리스트 보여줌
class MainView(ListView):
    model = Diary
    template_name = 'diary/diary.html'
    context_object_name = 'diarys'
    # paginate_by = 8
    ordering = ['-dt_created']

# 일기 세부 내용
class DiaryDetailView(DetailView):
    model = Diary
    template_name = 'diary/diary_detail.html'
    pk_url_kwarg = 'diary_id'

# 일기 작성
class DiaryCreateView(CreateView):
    model = Diary
    form_class = DiaryCreateForm
    template_name = 'diary/diary_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('diary-detail', kwargs={'diary_id':self.object.id})
    
    
# 일기 수정
class DiaryUpdateView(UpdateView):
    model = Diary
    form_class = DiaryCreateForm
    template_name = 'diary/diary_form.html'
    pk_url_kwarg = 'diary_id'
    
    def get_success_url(self):
        return reverse('diary-detail', kwargs={'diary_id':self.object.id})
    
class DiaryDeleteView(DeleteView):
    model = Diary
    template_name = 'diary/diary_delete.html'
    pk_url_kwarg = 'diary_id'
    
    def get_success_url(self):
        return reverse('main')