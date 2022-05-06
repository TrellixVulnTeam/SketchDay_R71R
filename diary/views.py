import email
import imp
from django.http import JsonResponse, HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils import timezone
from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation
# generic view
from django.views.generic import ListView, UpdateView, DeleteView
from numpy import rec
from sympy import Id
from braces.views import LoginRequiredMixin

from diary.models import Diary, Comment
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
        if user_id == self.request.user:
            return Diary.objects.filter(author__id = user_id).order_by('-dt_created')
        else:
            return Diary.objects.filter(public_TF=True, author__id = user_id).order_by('-dt_created')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = get_object_or_404(User, id=self.kwargs.get("user_id"))
        return context
        


@login_required
def diaryDetailView(request, diary_id):
    qs = get_object_or_404(Diary, pk=diary_id)
    db_music = get_object_or_404(Music, pk=qs.music_no)
    current_id = User.objects.get(email=qs.author).id
    db_rec_diary = get_object_or_404(Diary, pk=recommendation_ml.get_recommendation_diary(qs.vector, current_id))
    jsonDec = json.decoder.JSONDecoder()

    db_music.url = db_music.url[17:]
    comments = Comment.objects.filter(diary=diary_id)

    try:
        qs.emotion_value = jsonDec.decode(qs.emotion_value)
    except:
        pass
    context = {'diary': qs,
            'music': db_music,
            'rec_diary': db_rec_diary,
            'comments' : comments}

    return render(request, 'diary/diary_detail.html', context)




@login_required
def diaryCreateView(request, dt_selected=None):
    # 이메일 인증 여부
    if EmailAddress.objects.filter(user=request.user, verified=True).exists():
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
                    return redirect('diary-detail', diary_id= post.id)
                else:
                    messages.warning(request, '작성한 일기가 있습니다.')
                    return redirect('cal:calendar')
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
    else:
        # 이메일 재전송
        send_email_confirmation(request, request.user)
        return redirect("account_email_confirmation_required")

# 일기 수정
def diaryUpdateView(request, diary_id, dt_selected=None):
    object = get_object_or_404(Diary, id=diary_id)
    if request.method == 'POST':
        form = DiaryCreateForm(request.POST, instance=object)
        current_id = User.objects.get(id=request.user.id)
        if form.is_valid():
            post = form.save(commit=True)
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
                return redirect('diary-detail', diary_id= diary_id)
            else:
                messages.warning(request, '작성한 일기가 있습니다.')
                return redirect('diary-detail', diary_id= diary_id)
    else:
        form = DiaryCreateForm(instance = object)
    return render(request, 'diary/diary_form.html',{
        'form': form,
    })

# class DiaryUpdateView(UpdateView):
#     model = Diary
#     form_class = DiaryCreateForm
#     template_name = 'diary/diary_form.html'
#     pk_url_kwarg = 'diary_id'
    
#     def get_success_url(self):
#         return reverse('diary-detail', kwargs={'diary_id':self.object.id})



# 일기 삭제
class DiaryDeleteView(DeleteView):
    model = Diary
    template_name = 'diary/diary_delete.html'
    pk_url_kwarg = 'diary_id'
    
    def get_success_url(self):
        return reverse('cal:calendar')
    
# 추천 노래 평가
def rating(request) :
    # print('I an rating')
    if request.method == 'POST' :
        print(request)
        data = json.load(request)
        diary = Diary.objects.get(pk = data['diary_id'])
        music = Music.objects.get(pk = data['music_id'])
        
        rate = music.rate
        cnt = music.rate_cnt

        music.rate = (rate*cnt + float(data['score'])) / (cnt+1)
        music.rate_cnt = cnt+1
        diary.rate = True

        diary.save()
        music.save()

        return HttpResponse({'result':'success'})


@login_required
def comment_write_view(request, pk):
    diary = get_object_or_404(Diary, id=pk)
    writer = request.POST.get('writer')
    content = request.POST.get('content')
    if content:
        comment = Comment.objects.create(diary=diary, content=content, author=request.user, dt_created=timezone.now())
        comment.save()
        data = {
            'writer': writer,
            'content': content,
            'created': timezone.now(),
            'comment_id': comment.id
        }
        
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type = "application/json")

@login_required
def comment_delete_view(request, pk):
    post = get_object_or_404(Diary, id=pk)
    comment_id = request.POST.get('comment_id')
    target_comment = Comment.objects.get(pk = comment_id)

    if request.user == target_comment.author:
        target_comment.deleted = True
        target_comment.save()
        post.save()
        data = {
            'comment_id': comment_id,
        }
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type = "application/json")
