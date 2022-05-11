from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'cal'
urlpatterns = [
    url('', views.CalendarView.as_view(), name='calendar'),


    # url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)