from django.conf.urls import url, include

# REST
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.generic import TemplateView, RedirectView # для разработки
# REST

from .views import (
	home,
	# my_account,

	# * old
	# UnitsListView,
	# ScheduleListView,
	# UnitScheduleListView,
	# MyRecListView,

	# REST
	UnitUserProfileList,
	UnitUserProfileDetail,
	
	# actions with calendar
	schedule_calendar,

	# newREST
	UnitScheduleViewSet,


	# new rest rest
	event_detail,
	event_list,
	)

from rest_framework import routers
router = routers.SimpleRouter()
router.register(r'unit_schedule', UnitScheduleViewSet)

urlpatterns = [

	# actual rest urls
	url(r'^event_detail/(?P<pk>[0-9]+)$', event_detail, name='event_detail'),
	url(r'^event_list/(?P<unit>[0-9]+)$', event_list, name='event_list'),
	
	url(r'^$', RedirectView.as_view(url='units_list/')),


	url(r'^units_list/$', TemplateView.as_view(template_name='units/new_units_list.html'), name='units_list'),
	url(r'^units_list/(?P<unit>.*)/$', schedule_calendar, name='schedule_calendar'),

	# url(r'^schedule/$', ScheduleListView.as_view(), name='schedule_list'),
	# url(r'^myrecords/$', MyRecListView.as_view(), name='myrecords_list'),
	# url(r'^schedule/(?P<unit>.*)/$', UnitScheduleListView.as_view(), name='unit_schedule_list'),
]

urlpatterns += router.urls