from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from .models import UnitUserProfile, Unit, UnitReservation


class UnitReservationAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'unit',
        'start_work',
        'end_work',
        'tester',
        'reg_date',
        'edit_date',
        # 'contract',
        'test_object',
        )

class UnitAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'unit_name',
        'unit_manager',
        'parallel_records',
        'start_work',
        'end_work',
        'duration_of_record',
    )


class UnitUserProfileAdmin(admin.ModelAdmin):

    def fio(obj):
        fio = User.get_full_name(obj.user)
        return fio
    fio.short_description = u'ФИО'      
    
    def make_notice_me(self, request, queryset):
        queryset.update(notice_me=True)
    make_notice_me.short_description = u'Отметить "Получать уведомления"'
    
    def make_unnotice_me(self, request, queryset):
        queryset.update(notice_me=False)
    make_unnotice_me.short_description = u'Снять "Получать уведомления"'

    actions = ['make_notice_me', 'make_unnotice_me']

    list_display = (
        fio,
        # 'ntg',
        'tester',
        'boss',
        'superboss',
        'notice_me'
        )


admin.site.register(UnitUserProfile, UnitUserProfileAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(UnitReservation, UnitReservationAdmin)