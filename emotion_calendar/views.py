from datetime import datetime, timedelta, date
from django.views import generic
from django.utils.safestring import mark_safe
import calendar
from .utils import Calendar
from diary.models import *

# wordCloud
from wordcloud import WordCloud
class CalendarView(generic.ListView):
    model = Diary
    template_name = 'emotion_calendar/calendar.html'
    context_object_name = 'diarys'

    def get_context_data(self, **kwargs):
        # diarys = Diary()

        context = super().get_context_data(**kwargs)
        
        d = get_date(self.request.GET.get('month', None))
        diarys = Diary.objects.filter(author=self.request.user, dt_created__month=d.month)
        
        # 이번달 전체 일기 내용
        this_month_diary = ""
        for i in range(len(diarys)):
            this_month_diary += diarys[i].content
            this_month_diary += ' '

        wc = WordCloud(font_path='static/YdestreetB.ttf', width=400, height=400, scale=2.0, max_font_size=250)
        gen = wc.generate(this_month_diary)
        f_name = str(self.request.user).split('.')[0]
        full_name = 'static/'+ f_name +'.png'
        gen.to_file(full_name)
        down_name = '/../static/'+ f_name +'.png'
        context['img_path'] = down_name

        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(self.request.user, withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

class wordCloudView(generic.DetailView):
    model = User
    template_name = "emotion_calendar/calendar.html"
    pk_url_kwarg = 'user_id'
    context_object_name = "profile_user"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        context['user_diary'] = Diary.objects.filter(author__id = user_id).order_by("-dt_created")[:4]
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

