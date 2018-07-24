from datetime import datetime, timedelta
from pytz import timezone as pytz_timezone

from rest_framework import serializers

from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q

from units.models import UnitSchedule, Unit, LANGUAGE_CHOICES, STYLE_CHOICES, UnitUserProfile

msc_tz = pytz_timezone("Europe/Moscow")


class UnitUserProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UnitUserProfile
        fields = ('id', 'user', 'tester', 'boss',
                    # 'ntg',  'unit_schedule',
                  'superboss', 'notice_me',)

class UnitScheduleCreateSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.id')
    # owner = serializers.ReadOnlyField()
    owner = UnitUserProfileSerializer()
    start_work = serializers.DateTimeField()
    end_work = serializers.DateTimeField()

    class Meta:
        model = UnitSchedule
        fields = ('unit', 'start_work', 'end_work', 'tester','distance',
            # 'contract',
            'test_object', 'note_text', 'reg_date', 'edit_date',
            'owner')





class UnitScheduleUpdateSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    start_work = serializers.DateTimeField()
    end_work = serializers.DateTimeField()

    # мб это нужный айдишник????
    # id = serializers.IntegerField()

    def validate(self, data):
        start_time = data['start_work'].time()
        end_time = data['end_work'].time()
        day_of_record = data['start_work'].date()
        # day_of_record = data['start_work']

        print('-'*20)
        print('self', self)
        # print('self - pk', self.pk)
        print('*'*20)


        # print('ID', data ) 

        # print('self', self.get_pk_field() ) 
        # get_model_fields 
        print('*'*20)
        print('data', data)
        print('-'*20)

        if start_time >= end_time:
            raise serializers.ValidationError('Испытание должно начинаться ' +
                                              'раньше чем заканчиваться')
        if data['start_work'] < timezone.now():
            raise serializers.ValidationError('Вы пытаетесь записаться на прошедшее время')


        unit = Unit.objects.filter(unit_name=data['unit'])[0]

        if  start_time < unit.start_work or end_time > unit.end_work:
            raise serializers.ValidationError('Время испытания выходит за\
                 диапазон рабочего времени установки')


        # runtime warnings!!!
        # day_of_record = day_of_record.astimezone(msc_tz)
        # next_day = next_day.astimezone(msc_tz)

        # пришлось добавить один день, без этого фильтр не выбирал самый последний день возможной записи
        next_day = day_of_record + unit.duration_of_record + timedelta(days=1)

        if unit.parallel_records:
            # параллельные испытания
            queryset = UnitSchedule.objects.filter(unit=data['unit'],distance=data['distance']
                ).filter(start_work__gte=day_of_record, start_work__lte=next_day
                ).order_by('start_work').values_list('start_work','end_work') 
        else:
            queryset = UnitSchedule.objects.filter(unit=data['unit']
                ).filter(start_work__gte=day_of_record, start_work__lte=next_day
                ).order_by('start_work').values_list('start_work','end_work')  
        
        if len(queryset) == 0:
            return data
        for time_range in queryset:
            t1, t2 = time_range
            t1 = t1.astimezone(msc_tz)
            t2 = t2.astimezone(msc_tz)
            t1 = t1.time()
            t2 = t2.time()
            if start_time < t1 and end_time > t2:
                raise serializers.ValidationError('Внутри выбранного диапазона уже есть запись')
            if t1 < start_time and start_time < t2:
                raise serializers.ValidationError('Start внутри другой записи')
            if end_time > t1 and t2 > end_time:
                raise serializers.ValidationError('End внутри другой записи')    
        return data


    class Meta:
        model = UnitSchedule
        fields = ('unit', 'start_work', 'end_work', 'tester', 'distance',
            # 'contract',
            'test_object', 'note_text', 'reg_date', 'edit_date', 'owner', 'id')





class ScheduleEventUpdateSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    start_work = serializers.DateTimeField()
    end_work = serializers.DateTimeField()

    class Meta:
        model = UnitSchedule
        fields = (
            'unit',
            'start_work', 'end_work',
            'tester', 'distance',
            # 'contract',
            'test_object',
            'note_text',
            # 'reg_date', 'edit_date',
            'owner', 'id')




class UnitScheduleListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    start = serializers.DateTimeField(source='get_start_work')
    end = serializers.DateTimeField(source='get_end_work')
    tester = serializers.CharField(source='get_tester')
    distance = serializers.CharField(source='get_distance')
    # передаю title в объект event
    title = owner
    color = serializers.ReadOnlyField(source='get_color')
    distance_num = serializers.ReadOnlyField(source='get_distance_num')
    tester_id = serializers.ReadOnlyField(source='get_tester_id')
    owner_full_name = serializers.ReadOnlyField(source='get_owner_full_name')

    class Meta:
        model = UnitSchedule
        fields = ('id', 'unit', 'start', 'end', 'tester','distance',
            # 'contract',
            'test_object', 'note_text', 'reg_date', 'edit_date', 'owner',
            'title', 'color', 'distance_num', 'tester_id', 'owner_full_name')








    # def validate(self, data):
    #     start_time = data['start_work'].time()
    #     end_time = data['end_work'].time()
    #     day_of_record = data['start_work'].date()
    #     # day_of_record = data['start_work']

    #     print('self', self)
    #     print('data', data)


    #     if start_time >= end_time:
    #         raise serializers.ValidationError('Испытание должно начинаться ' +
    #                                           'раньше чем заканчиваться')
    #     if data['start_work'] < timezone.now():
    #         raise serializers.ValidationError('Вы пытаетесь записаться на прошедшее время')


    #     unit = Unit.objects.filter(unit_name=data['unit'])[0]

    #     if  start_time < unit.start_work or end_time > unit.end_work:
    #         raise serializers.ValidationError('Время испытания выходит за\
    #              диапазон рабочего времени установки')


    #     # runtime warnings!!!
    #     # day_of_record = day_of_record.astimezone(msc_tz)
    #     # next_day = next_day.astimezone(msc_tz)

    #     # пришлось добавить один день, без этого фильтр не выбирал самый последний день возможной записи
    #     next_day = day_of_record + unit.duration_of_record + timedelta(days=1)

    #     if unit.parallel_records:
    #         # параллельные испытания
    #         queryset = UnitSchedule.objects.filter(unit=data['unit'],distance=data['distance']
    #             ).filter(start_work__gte=day_of_record, start_work__lte=next_day
    #             ).order_by('start_work').values_list('start_work','end_work') 
    #     else:
    #         queryset = UnitSchedule.objects.filter(unit=data['unit']
    #             ).filter(start_work__gte=day_of_record, start_work__lte=next_day
    #             ).order_by('start_work').values_list('start_work','end_work')  
    
    #     print('я туть')
        
    #     if len(queryset) == 0:
    #         return data
    #     for time_range in queryset:
    #         t1, t2 = time_range
    #         t1 = t1.astimezone(msc_tz)
    #         t2 = t2.astimezone(msc_tz)
    #         t1 = t1.time()
    #         t2 = t2.time()
    #         if start_time < t1 and end_time > t2:
    #             raise serializers.ValidationError('Внутри выбранного диапазона уже есть запись')
    #         if t1 < start_time and start_time < t2:
    #             raise serializers.ValidationError('Start внутри другой записи')
    #         if end_time > t1 and t2 > end_time:
    #             raise serializers.ValidationError('End внутри другой записи')    
    #     return data
