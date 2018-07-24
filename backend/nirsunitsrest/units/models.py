# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

from django.contrib.auth.models import User

import datetime

from datetime import timedelta as timedelta_dt
from datetime import time

from django.utils import timezone

# from contracts.models import Contract
# from budget.models import NTGroup

def get_all_users_emails():
    all_testers = UnitUserProfile.objects.filter(notice_me=True)
    email_list = [user.user.email for user in all_testers]
    email_list.sort()
    return email_list


def send_email(my_email, subject):
    send_to = my_email.unit.unit_notice_users_emails()
    send_to.append(my_email.tester.email)
    ntg = my_email.tester.units_profile.ntg
    email_subject = subject + u' %s' % my_email.unit
    email_message = u'''
    
    Испытатель: %s %s
    Установка: %s
    Время начала: %s
    Время окончания: %s
    Группа: %s
    Договор: %s
    Объект: %s
    Примечание: %s

    Система записи на установки
    АО "ЭНПО СПЭЛС"
            ''' % (
        my_email.tester.last_name,
        my_email.tester.first_name,
        my_email.unit,
        my_email.start_work.strftime("%d.%m.%Y %H:%M"),
        my_email.end_work.strftime("%d.%m.%Y %H:%M"),
        ntg.ntg,
        my_email.contract,
        my_email.test_object,
        my_email.note_text,
        )
    send_mail(
        email_subject,
        email_message,
        'units@stoikost.mephi.ru',
        send_to,
        fail_silently=False,
        )


def send_email_to_all(my_email, subject, start_time=None, stop_time=None):
    send_to = get_all_users_emails()
    email_subject = subject
    if start_time and stop_time:
        my_start_time = start_time.strftime("%d.%m.%Y %H:%M")
        my_stop_time = stop_time.strftime("%d.%m.%Y %H:%M")
    else:
        my_start_time = my_email.start_work.strftime("%d.%m.%Y %H:%M")
        my_stop_time = my_email.end_work.strftime("%d.%m.%Y %H:%M")
    email_message = u'''
    
    Освободилось время для работы на установке - %s!!!

    Испытатель: %s %s
    Время начала: %s
    Время окончания: %s

    Система записи на установки
    АО "ЭНПО СПЭЛС"
    
    PS Вы можете отписаться от рассылки по ссылке: http://portal.spels.ru/units/myaccount/
            ''' % (
        my_email.unit,
        my_email.tester.last_name,
        my_email.tester.first_name,
        my_start_time,
        my_stop_time
        )
    send_mail(
        email_subject,
        email_message,
        'units@stoikost.mephi.ru',
        send_to,
        fail_silently=False,
        )


class Unit(models.Model):
    unit_name = models.CharField('Наименование', unique=True, max_length=100)
    unit_manager = models.ForeignKey(User, related_name='unit_manager', verbose_name='Начальник установки')
    unit_notice_users = models.ManyToManyField(User, related_name = 'unit_notice', verbose_name='Уведомления', blank = True)
    note_text = models.TextField('Примечания', blank = True, null = True)
    # режим работы
    parallel_records = models.BooleanField(default=False)
    # временной режим работы
    start_work = models.TimeField(verbose_name='Время начала работы установки', default=time(9,0))
    end_work = models.TimeField(verbose_name='Время окончания работы установки', default=time(21,0))
    # длительность записи в днях
    duration_of_record = models.DurationField(verbose_name='Длительность записи', default=timedelta_dt(days=1))


    def unit_notice_users_emails(self):
        email_list = [user.email for user in self.unit_notice_users.all()]
        email_list.append(self.unit_manager.email)
        email_list.sort()
        return email_list

    unit_notice_users_emails.short_description = u'Уведомления'    

    def __str__(self):
        return self.unit_name

    class Meta:
        ordering = ['unit_name']
        verbose_name = u'Установка'
        verbose_name_plural = u'Установки'

def get_busy_dates(unit=None):
    if unit:
        busy_dates_start = UnitSchedule.objects.filter(unit=unit, start_work__date__gte=timezone.now().date()).dates('start_work', 'day')
        busy_dates_end = UnitSchedule.objects.filter(unit=unit, end_work__date__gte=timezone.now().date()).dates('end_work', 'day')
        busy_dates = list(busy_dates_start)
        busy_dates.extend(list(busy_dates_end))
        busy_dates.sort()
    else:
        busy_dates = []
    return busy_dates

def get_free_date(unit=None):
    if unit:
        busy_dates = get_busy_dates(unit)
        start_date = timezone.now().date()
        if start_date.month >= 10:
            end_month = 12
        else:
            end_month = start_date.month + 3
        end_date = datetime.date(start_date.year, end_month, 1)
        day_count = (end_date - start_date).days + 1
        for single_date in [d for d in (start_date + datetime.timedelta(n) for n in range(day_count)) if d <= end_date]:
            if (single_date not in busy_dates) and (single_date.weekday() not in [5,6]):
                return single_date
    return timezone.now()+datetime.timedelta(days=1)


# REST

from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class UnitSchedule(models.Model):
    unit = models.ForeignKey(Unit, verbose_name = "Установка")
    start_work = models.DateTimeField("Дата и время начала работы")
    end_work = models.DateTimeField("Дата и время окончания работы")
    tester = models.ForeignKey(User, verbose_name="Испытатель")
    # contract = models.ForeignKey(Contract, verbose_name="Договор", on_delete=models.PROTECT)
    test_object = models.CharField("Объект испытаний", max_length = 20)
    DISTANCE_CHOICES = (
        (1, u'малое'),
        (2, u'среднее'),
        (3, u'большое'),
        )
    distance = models.IntegerField("Расстояние", choices = DISTANCE_CHOICES, blank = False, null = True, default=2)
    note_text = models.TextField('Примечания', help_text = u"Укажите режим и требуемые уровни", blank = True, null = True)
    reg_date = models.DateTimeField('Дата регистрации', auto_now_add = True, auto_now = False)
    edit_date = models.DateTimeField('Дата изменений', auto_now_add = False, auto_now = True)
    owner = models.ForeignKey('auth.User', related_name='unit_schedule', on_delete=models.CASCADE)

    def __str__(self):
        return u"%s-%s на %s" % (self.unit, self.tester.last_name, self.start_work.date())

    @property
    def is_past_due(self):
        return timezone.now() > self.end_work

    # небольшое конвертирование полей класса для удобной сериализации
    # можно изменить поля класса на start & end и не использоватать эти две функции
    def get_start_work(self):
        return self.start_work

    def get_end_work(self):
        return self.end_work   

    def get_distance_num(self):
        return self.distance    

    # get value by key 
    def get_distance(self):
        return dict(self.DISTANCE_CHOICES)[self.distance]
        
    def get_tester(self):
        return self.tester 

    def get_tester_id(self):
        return self.tester.id        

    BACKGROUND_COLORS = ['#00ff00', 'yellow', 'red']
    def get_owner_full_name(self):
        full_name = self.owner.first_name + ' ' + self.owner.last_name
        return full_name

    def get_color(self):
        return self.BACKGROUND_COLORS[self.distance - 1]       
            
    class Meta:
        ordering = ['-start_work']
        verbose_name = u'Запись на установку'
        verbose_name_plural = u'Запись на установки'


class UnitUserProfile(models.Model):
    user = models.OneToOneField(User, related_name='units_profile')
    # ntg = models.ForeignKey(NTGroup, verbose_name = "НТГ", related_name = 'ntg_unit')
    tester = models.BooleanField("Испытатель", default=True)
    boss = models.BooleanField("Руководитель НТГ", default=False)
    superboss = models.BooleanField("Начальство", default=False)
    notice_me = models.BooleanField("Получать уведомления", default=False)
    note_text = models.TextField("Примечания", blank = True, null = True)

    def get_fio(self):
        fio = "%s %.1s." % (self.user.last_name, self.user.first_name)
        return fio

    def __str__(self):
        return self.get_fio()

    class Meta:
        ordering = ['user']
        verbose_name = u'Профайл'
        verbose_name_plural = u'Профайлы'