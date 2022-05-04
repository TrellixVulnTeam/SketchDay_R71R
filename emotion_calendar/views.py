from datetime import datetime, timedelta, date
from django.views import generic
from django.utils.safestring import mark_safe
import calendar
from .utils import Calendar
from diary.models import *


class CalendarView(generic.ListView):
    model = Diary
    template_name = 'emotion_calendar/calendar.html'
    context_object_name = 'diarys'

    def get_context_data(self, **kwargs):
        # diarys = Diary()

        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        user_id = self.kwargs.get('user_id')
        # diarys = context.filter(dt_created__month=d)
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(self.request.user, withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context
    
    # def get_queryset(self):
    #     d = get_date(self.request.GET.get('month', None))
    #     diarys = super().get_queryset().filter(dt_created__month=d)
    #     print(diarys)
    #     return diarys

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

