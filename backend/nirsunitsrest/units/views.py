from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect, get_object_or_404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.db.models import Q

from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator

from django.contrib import messages

from django.utils import timezone
from datetime import datetime

from .models import (
    get_busy_dates,
    get_free_date,
    UnitUserProfile,
    Unit,
    UnitSchedule,
    )


def check_access_app(user):
    check = UnitUserProfile.objects.filter(user=user)
    if len(check) > 0:
        a = True
    else:
        a = False
    return a


def make_message_text(unit, start_work):
    queryset = UnitSchedule.objects.filter(unit=unit).filter(
        Q(start_work__startswith=start_work.date())|
        Q(end_work__startswith=start_work.date())
        ).order_by('start_work').values_list('tester__last_name', 'start_work', 'end_work')
    if len(queryset) > 1:
        my_table = u"<br/><table class='table'><tr><th>Испытатель</th><th>Время начала</th><th>Время окончания</th></tr>"
        for t in queryset:
            if t[1].date() < start_work.date():
                my_table += u"<tr><td>%s</td><td>-</td><td>%s</td></tr>" % (t[0], t[2].strftime("%H:%M"))
            elif t[2].date() > start_work.date():
                my_table += u"<tr><td>%s</td><td>%s</td><td>-</td></tr>" % (t[0], t[1].strftime("%H:%M"))
            else:
                my_table += u"<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (t[0], t[1].strftime("%H:%M"), t[2].strftime("%H:%M"))
        text_message = u"""
            <h2>Ваша запись УСЛОВНА! Требует согласования!</h2><br/>
            <h3>Записи в этот день (%s):</h3>""" % t[1].strftime("%d.%m.%Y") + my_table + "</table>"
        return text_message
    else:
        return False

@login_required()
@user_passes_test(check_access_app, '/accessdenied/', None)
def home(request):
    my_role = request.user.units_profile
    if my_role.boss:
        return redirect('units:units_list')
    else:
        return redirect('units:myrecords_list')


class UnitsListView(ListView):
    model = Unit
    template_name = "units/units_list.html"
    paginate_by = 15

    @method_decorator(login_required)
    @method_decorator(user_passes_test(check_access_app, '/accessdenied/', None))
    def dispatch(self, *args, **kwargs):
        return super(UnitsListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UnitsListView, self).get_context_data(**kwargs)
        context['location'] = 'units_list'
        return context

class ScheduleListView(ListView):
    model = UnitSchedule
    template_name = "units/schedule_list.html"
    paginate_by = 15

    @method_decorator(login_required)
    @method_decorator(user_passes_test(check_access_app, '/accessdenied/', None))
    def dispatch(self, *args, **kwargs):
        return super(ScheduleListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            queryset = super(ScheduleListView, self).get_queryset().filter(
                Q(unit__unit_name__icontains=query) |
                Q(tester__units_profile__ntg__ntg__icontains=query) |
                Q(tester__last_name__icontains=query) |
                Q(contract__contract_num__icontains=query) |
                Q(test_object__icontains=query)
                )
        else:
            queryset = super(ScheduleListView, self).get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ScheduleListView, self).get_context_data(**kwargs)
        context['table_title'] = 'График работы на всех установках'
        context['location'] = 'schedule_list'
        return context


class UnitScheduleListView(ListView):
    model = UnitSchedule
    template_name = "units/schedule_list.html"
    paginate_by = 15

    @method_decorator(login_required)
    @method_decorator(user_passes_test(check_access_app, '/accessdenied/', None))
    def dispatch(self, *args, **kwargs):
        return super(UnitScheduleListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        query = self.request.GET.get("q")
        my_unit = self.kwargs['unit']
        if query:
            queryset = super(UnitScheduleListView, self).get_queryset().filter(unit__unit_name=my_unit).filter(
                Q(tester__units_profile__ntg__ntg__icontains=query) |
                Q(tester__last_name__icontains=query) |
                Q(contract__contract_num__icontains=query) |
                Q(test_object__icontains=query)
                )
        else:
            queryset = super(UnitScheduleListView, self).get_queryset().filter(unit__unit_name=my_unit)
        return queryset

    def get_context_data(self, **kwargs):
        my_unit = self.kwargs['unit']
        context = super(UnitScheduleListView, self).get_context_data(**kwargs)
        context['table_title'] = u'График работы на %s' % my_unit
        context['location'] = 'unit_schedule_list'
        context['unit_name'] = my_unit
        return context


class MyRecListView(ListView):
    model = UnitSchedule
    template_name = "units/schedule_list.html"
    paginate_by = 15

    @method_decorator(login_required)
    @method_decorator(user_passes_test(check_access_app, '/accessdenied/', None))
    def dispatch(self, *args, **kwargs):
        return super(MyRecListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        today = timezone.now()
        tester=self.request.user
        query = self.request.GET.get("q")
        if self.request.GET.get("all") == "1":
            all_recs = True
        else:
            all_recs = False
        if query and all_recs:
            queryset = super(MyRecListView, self).get_queryset().filter(tester=tester).filter(
                Q(unit__unit_name__icontains=query) |
                Q(contract__contract_num__icontains=query) |
                Q(test_object__icontains=query)
                ).order_by('start_work')
        elif query:
            queryset = super(MyRecListView, self).get_queryset().filter(tester=tester, start_work__gte=today).filter(
                Q(unit__unit_name__icontains=query) |
                Q(contract__contract_num__icontains=query) |
                Q(test_object__icontains=query)
                ).order_by('start_work')
        elif all_recs:
            queryset = super(MyRecListView, self).get_queryset().filter(tester=tester).order_by('start_work')
        else:
            queryset = super(MyRecListView, self).get_queryset().filter(tester=tester, start_work__gte=today).order_by('start_work')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MyRecListView, self).get_context_data(**kwargs)
        context['table_title'] = 'Мои записи'
        context['location'] = 'myrecords_list'
        return context


# @login_required()
# @user_passes_test(check_access_app, '/accessdenied/', None)
# def record_edit(request, pk=None):
#     my_role = request.user.units_profile
#     if my_role.tester:
#         record = get_object_or_404(UnitSchedule, pk=pk)
#         if record.tester == request.user:
#             form = RecordForm(request.POST or None, instance=record)
#             if request.method == 'POST':
#                 if form.is_valid():
#                     instance = form.save(commit = False)
#                     instance.save()
#                     text_message = make_message_text(instance.unit, instance.start_work)
#                     if text_message:
#                         messages.info(request, text_message, extra_tags='html_save')
#                     return redirect('units:myrecords_list')



# @login_required()
# @user_passes_test(check_access_app, '/accessdenied/', None)
# def record_add(request, unit = None):
#     my_role = request.user.units_profile
#     if my_role.tester:
#         today_y = timezone.now().year
#         today_m = timezone.now().month
#         today_d = timezone.now().day
#         if unit:
#             my_unit = get_object_or_404(Unit, unit_name = unit)
#             free_date = get_free_date(my_unit)
#             busy_dates = get_busy_dates(my_unit)
#             disabledDates = []
#             for busy_date in busy_dates:
#                 disabledDates.append(busy_date.strftime('%m/%d/%Y'))
#             initial = {
#                 'unit': my_unit,
#                 'start_work': datetime(free_date.year, free_date.month, free_date.day, 11),
#                 'end_work': datetime(free_date.year, free_date.month, free_date.day, 20),
#                 'tester': request.user,
#                 }
#         else:
#             disabledDates = []
#             initial = {
#                 'start_work': datetime(today_y, today_m, today_d + 1 ,11),
#                 'end_work': datetime(today_y, today_m, today_d + 1 ,20),
#                 'tester': request.user,
#                 }
#         minDate = datetime(today_y, today_m, today_d).strftime('%m/%d/%Y')
#         form = RecordForm(request.POST or None, initial=initial)
#         if request.method == 'POST':
#             if form.is_valid():
#                 instance = form.save(commit = False)
#                 instance.save()
#                 text_message = make_message_text(instance.unit, instance.start_work)
#                 if text_message:
#                     messages.info(request, text_message, extra_tags='html_save')
#                 return redirect('units:myrecords_list')






@login_required()
@user_passes_test(check_access_app, '/accessdenied/', None)
def record_print(request, pk=None):
    record = get_object_or_404(UnitSchedule, pk=pk)
    content = {
        'obj': record,
        'location' : 'record_print',
    }
    return render(request, "units/print.html", content)


# @login_required()
# @user_passes_test(check_access_app, '/accessdenied/', None)
# def my_account(request):
#     my_role = request.user.units_profile
#     if my_role.tester:
#         record = get_object_or_404(UnitUserProfile, user=request.user)
#         form = MyAccountForm(request.POST or None, instance=record)
#         if request.method == 'POST':
#             if form.is_valid():
#                 instance = form.save(commit = False)
#                 instance.save()
#                 return redirect('units:myrecords_list')
#         content = {
#             'header': 'Личный кабинет',
#             'title': 'Настройки',
#             'button': 'Сохранить',
#             'form': form,
#             'location' : 'my_account',
#         }
#         return render(request, "units/form-center.html", content)
#     else:
#         raise Http404



# REST
from units.models import UnitSchedule
from units.serializers import UnitUserProfileSerializer 
from rest_framework import generics
from django.contrib.auth.models import User

from rest_framework import permissions
from units.permissions import IsOwnerOrReadOnly


class UnitUserProfileList(generics.ListAPIView):
    queryset = UnitUserProfile.objects.all()
    serializer_class = UnitUserProfileSerializer


class UnitUserProfileDetail(generics.RetrieveAPIView):
    queryset = UnitUserProfile.objects.all()
    serializer_class = UnitUserProfileSerializer


import re
def  schedule_calendar(request, unit=None):
    """
    Рендерим страницу с календарем

    testers - для отображения списка испытателей при записи на испытание
    unit - достаем id установки, на которой собираемся проводить испытание 
        и отправляем его по ajax-запросу для создания записи
    """

    # костыль
    unit = re.split(r'/',unit)[0]
    testers = UnitUserProfile.objects.filter(tester=True)
    if unit:
        unit = Unit.objects.filter(unit_name=unit)[0]
    return render(request, 'units/calendar.html', {'unit':unit, 'testers':testers})


# new REST
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from units.serializers import UnitScheduleCreateSerializer, UnitScheduleListSerializer, UnitScheduleUpdateSerializer
from units.permissions import IsOwnerOrReadOnly


class UnitScheduleViewSet(viewsets.ModelViewSet):
    queryset = UnitSchedule.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)    


    def get_serializer_class(self):
        if self.action == 'list':
            return UnitScheduleListSerializer
        if self.action == 'create':
            return UnitScheduleCreateSerializer
        if self.action == 'update':
            return UnitScheduleUpdateSerializer
        return UnitScheduleCreateSerializer


    def list(self, request, *args, **kwargs):
        """
        переопределил эту функцию, добавив фильтр по установкам (чтобы лишнее не присылала)
        """
        unit_pk = request.query_params['unit']
        unit_name = Unit.objects.filter(pk=unit_pk)[0]
        new_query_set = UnitSchedule.objects.filter(unit=unit_name)
        
        page = self.paginate_queryset(new_query_set)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(new_query_set, many=True)
        return Response(serializer.data)   




from rest_framework import status
from rest_framework.decorators import api_view
from units.serializers import ScheduleEventUpdateSerializer
from .utils.validation import time_validation



@api_view(['GET', 'POST'])
def event_list(request, unit):
    """
    # 
    """
    if request.method == 'GET':

        

        unit_name = Unit.objects.filter(pk=unit)[0]
        print(unit_name)
        events_set = UnitSchedule.objects.filter(unit=unit_name)

        serializer = UnitScheduleListSerializer(events_set, many=True)
        return Response(serializer.data)


    elif request.method == 'POST':
        serializer = UnitScheduleCreateSerializer(data=request.data)
        user_serializer = UnitUserProfileSerializer(data=request.user)

        print('*'*30)
        b = time_validation(
            start=request.data['start_work'],
            end=request.data['end_work'],
            unit_pk=unit
        )
        print('*'*15)
        print('is VALID', b)
        print('*'*30)

        if b & serializer.is_valid():

            # print(serializer.data)
            print('userSerializer', user_serializer)
            print(request.user)

            serializer.save(owner=request.user)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def event_detail(request, pk):
    """
    Get, udpate, delete
    """
    try:
        schedule_event = UnitSchedule.objects.get(pk=pk)
    except UnitSchedule.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        serializer = ScheduleEventUpdateSerializer(schedule_event)
        return Response(serializer.data)


    elif request.method == 'PUT':
        serializer = ScheduleEventUpdateSerializer(schedule_event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
            # тут делаем валидацию
            print('serializer.is_valid', serializer)
        else:
            return Response(
                serilizer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        schedule_event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)