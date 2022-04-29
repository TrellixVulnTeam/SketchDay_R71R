from calendar import HTMLCalendar
from datetime import datetime, timedelta

from diary.models import Diary
from regex import E


class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, diarys):
		
		img_url = '''<a href="/diary/new"></a>'''
		diary = diarys.filter(dt_created__day=day)

		if diary:
			emotion = diary[0].emotion

			img_url += '<center><img src=/static/emotion_calendar/emotion/'

			if emotion == '행복':
				img_url += 'happy.jpg'
			elif emotion == '불안':
				img_url += 'unrest.jpg'
			elif emotion == '분노':
				img_url += 'anger.jpg'
			elif emotion == '슬픔':
				img_url += 'sad.jpg'
			else:
				img_url += 'tranquility.jpg'
			img_url += '></center>'

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {img_url} </ul></td>"
		return '<td></td>'

	# formats a week as a tr
	def formatweek(self, theweek, diarys):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, diarys)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, user, withyear=True):
		diarys = Diary.objects.filter(author=user, dt_created__month=self.month)
		
		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, diarys)}\n'

		return cal
