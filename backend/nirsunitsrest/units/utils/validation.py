from datetime import datetime, timedelta
from pytz import timezone as pytz_timezone

from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q

from units.models import UnitSchedule, Unit

msc_tz = pytz_timezone("Europe/Moscow")


def time_validation(start, end, unit_pk, distance=None, eventID=None):

    start_time = datetime.strptime(start, "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(end, "%Y-%m-%d %H:%M")
    
    # как то не очень...
    now = timezone.now()
    now = now.strftime("%Y-%m-%d %H:%M")
    now = datetime.strptime(now, "%Y-%m-%d %H:%M")

    if start_time >= end_time:
        raise serializers.ValidationError('Испытание должно начинаться ' +
                                        'раньше чем заканчиваться')
    if start_time < now:
        raise serializers.ValidationError('Вы пытаетесь записаться на прошедшее время')


    unit = Unit.objects.filter(pk=unit_pk)[0]
    if  start_time.time() < unit.start_work or end_time.time() > unit.end_work:
        raise serializers.ValidationError('Время испытания выходит за' +
                                        'диапазон рабочего времени установки')




    # runtime warnings!!!
    day_of_record = start_time.date()
    print(day_of_record, 'day_of_record')
    # day_of_record = day_of_record.astimezone(msc_tz)
    # next_day = next_day.astimezone(msc_tz)

    # пришлось добавить один день, без этого фильтр не выбирал самый последний день возможной записи
    next_day = day_of_record + unit.duration_of_record + timedelta(days=1)




    if unit.parallel_records:
        # параллельные испытания
        queryset = UnitSchedule.objects.filter(unit=unit,distance=distance
            ).filter(start_work__gte=day_of_record, start_work__lte=next_day
            ).order_by('start_work').values_list('start_work','end_work')
    else:
        queryset = UnitSchedule.objects.filter(unit=unit
            ).filter(start_work__gte=day_of_record, start_work__lte=next_day
            ).order_by('start_work').values_list('start_work','end_work')  
    
    if len(queryset) == 0:
        # return data
        return True
    # for time_range in queryset:
    #     t1, t2 = time_range
    #     t1 = t1.astimezone(msc_tz)
    #     t2 = t2.astimezone(msc_tz)
    #     t1 = t1.time()
    #     t2 = t2.time()
    #     if start_time < t1 and end_time > t2:
    #         raise serializers.ValidationError('Внутри выбранного диапазона уже есть запись')
    #     if t1 < start_time and start_time < t2:
    #         raise serializers.ValidationError('Start внутри другой записи')
    #     if end_time > t1 and t2 > end_time:
    #         raise serializers.ValidationError('End внутри другой записи')    
    # # return data
    return True
