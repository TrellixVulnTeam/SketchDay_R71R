from django.shortcuts import render
from django.urls import reverse
# generic view
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from diary.models import Diary
from diary.forms import DiaryCreateForm

from .ml_models import emotional_analysis
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

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
# class DiaryCreateView(CreateView):
#     model = Diary
#     form_class = DiaryCreateForm
#     template_name = 'diary/diary_form.html'
#     # emotion_model = emotional_analysis.EmotionAnalysis()
#     # model.emotion = emotion_model.predict({"data":model.content})

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)
    
#     def get_success_url(self):
#         return reverse('diary-detail', kwargs={'diary_id':self.object.id})

# 일기 작성 - 감정분석 수행되도록 수정
@login_required
def diaryCreateView(request):
    if request.method == 'POST':
        form = DiaryCreateForm(request.POST)
        if form.is_valid():
            # post = form.save(commit=True)
            post = form.save(commit=False)
            post.author = request.user  # 현재 로그인 user instance
            emotion_model = emotional_analysis.EmotionAnalysis()
            post.emotion = emotion_model.predict({"data":post.content})
            post.save()
            messages.success(request, '포스팅을 저장했습니다.')
            return redirect('main')
    else:
        form = DiaryCreateForm()

    return render(request, 'diary/diary_form.html',{
        'form': form,
        'post': None,
    })

# 일기 수정
class DiaryUpdateView(UpdateView):
    model = Diary
    form_class = DiaryCreateForm
    template_name = 'diary/diary_form.html'
    pk_url_kwarg = 'diary_id'
    
    def get_success_url(self):
        return reverse('diary-detail', kwargs={'diary_id':self.object.id})

# 일기 삭제
class DiaryDeleteView(DeleteView):
    model = Diary
    template_name = 'diary/diary_delete.html'
    pk_url_kwarg = 'diary_id'
    
    def get_success_url(self):
        return reverse('main')