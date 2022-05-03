from calendar import HTMLCalendar
from datetime import datetime, timedelta
from diary.models import Diary
import datetime

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		self.img_dic = {
			'행복' : 'happy.jpg',
			'불안' : 'unrest.jpg',
			'분노' : 'anger.jpg',
			'슬픔' : 'sad.jpg',
			'평온' : 'tranquility.jpg'
		}
		super(Calendar, self).__init__()


	def formatday(self, day, diarys):		
		img_url = ''
		diary = diarys.filter(dt_created__day=day)
		dt_selected = ''

		if diary.exists():
			emotion = diary[0].emotion
			img_url = f'<center><img width="50" height="50" src=/static/emotion_calendar/emotion/{self.img_dic[emotion]}></center>'
			onclick_url = f'"/diary/detail/{diary[0].id}"'
		else:
			dt_selected = f'{self.year}-{self.month}-{day}'
			onclick_url = f'"/diary/new/{dt_selected}"'

		if day != 0:
			return f'''<td onClick='location.href={onclick_url}' style="cursor:pointer;"><span class='date'>{day}</span><ul>{img_url} {dt_selected}</ul></td>'''
		return '<td></td>'


	def formatweek(self, theweek, diarys):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, diarys)
		return f'<tr> {week} </tr>'


	def formatmonth(self, user, withyear=True):
		diarys = Diary.objects.filter(author=user, dt_created__month=self.month)
		
		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, diarys)}\n'

		return cal
