import email
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
# generic view
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from numpy import rec
from sympy import Id
from braces.views import LoginRequiredMixin

from diary.models import Diary
from diary.models import Music
from Login.models import User
from diary.forms import DiaryCreateForm

from .ml_models import emotional_analysis
from .ml_models import recommendation_ml
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from diary import apps

from .ml_models.make_text2art import make_prompts
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()

import json
import datetime

# Create your views here.

# 전체 일기 리스트
class MainView(ListView):
    model = Diary
    template_name = 'diary/diary.html'
    context_object_name = 'diarys'
    paginate_by = 8
    def get_queryset(self):
        return Diary.objects.filter(public_TF=True).order_by('-dt_created')

# 내 일기 전체
class UserDiaryListView(ListView):
    model = Diary
    template_name = 'diary/user_diary_list.html'
    context_object_name = 'user_diarys'
    paginate_by = 8
    
    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        return Diary.objects.filter(author__id = user_id).order_by('-dt_created')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = get_object_or_404(User, id=self.kwargs.get("user_id"))
        return context
        
    
# 일기 세부 내용
# class DiaryDetailView(DetailView):
#     model = Diary
#     template_name = 'diary/diary_detail.html'
#     pk_url_kwarg = 'diary_id'
#     # model.emotion_value = jsonDec.decode(model.emotion_value)
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         jsonDec = json.decoder.JSONDecoder()
#         context['emotion_value'] = [0,1]
#         return context

@login_required
def diaryDetailView(request, diary_id):
    qs = get_object_or_404(Diary, pk=diary_id)
    db_music = get_object_or_404(Music, pk=qs.music_no)
    
    jsonDec = json.decoder.JSONDecoder()

    try:
        qs.emotion_value = jsonDec.decode(qs.emotion_value)
    except:
        pass
    context = {'diary': qs,
               'music': db_music}

    return render(request, 'diary/diary_detail.html', context)

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
def diaryCreateView(request, dt_selected=None):
    if request.method == 'POST':
        form = DiaryCreateForm(request.POST)
        current_id = User.objects.get(id=request.user.id)
        if form.is_valid():
            # post = form.save(commit=True)
            post = form.save(commit=False)
            post.author = request.user  # 현재 로그인 user instance
            post.vector = recommendation_ml.get_vector(post.content)
            post.music_no = recommendation_ml.get_recommendation(post.vector)
            emotion_model = emotional_analysis.EmotionAnalysis()
            emotion_val = emotion_model.predict({"data":post.content})
            post.emotion = emotion_val[1]
            # print(emotion_val[0])
            # print(type(emotion_val[0]))
            post.emotion_value = json.dumps(emotion_val[0])

            # prompt text 생성
            text = make_prompts(post.content, emotion_val[1])
            # background task에 전달
            nick = User.objects.get(email=request.user).nickname

            try:
                today = Diary.objects.get(author_id = current_id, dt_created = post.dt_created)
            except ObjectDoesNotExist:
                today = 1
            if today == 1:
                post.save()
                async_to_sync(channel_layer.send)('background_tasks', {'type':'sketch', 'prompts':text, 'userId':nick, 'diaryID':post.id})

                messages.success(request, '일기를 저장했습니다.')
                return redirect('main')
            else:
                messages.warning(request, '작성한 일기가 있습니다.')
                return redirect('main')
    else:
        if dt_selected:
            year, month, day = map(int, dt_selected.split('-'))
            init_date = datetime.date(year, month, day)
            form = DiaryCreateForm(initial={'dt_created' : init_date})
        else:
            form = DiaryCreateForm()

    return render(request, 'diary/diary_form.html',{
        'form': form,
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
    
