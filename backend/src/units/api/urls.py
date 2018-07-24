from django.conf.urls import url

from .views import (
    UnitReservationListAPIView,
    UnitReservationAPIDetailView
)

urlpatterns = [
    url(r'^$', UnitReservationListAPIView.as_view()),
    url(r'^(?P<pk>\d+)/$', UnitReservationAPIDetailView.as_view())
]
