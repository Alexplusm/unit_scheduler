from django.conf.urls import url

from .views import task_list, task_detail

urlpatterns = [
    url(r'^tasks/$', task_list, name='task_list'),
    url(r'^tasks/(?P<pk>[0-9]+)$', task_detail, name='task_detail'),
]