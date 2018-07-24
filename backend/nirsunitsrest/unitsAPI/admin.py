from django.contrib import admin

# Register your models here.
from .models import Task


class UnitAPIScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'completed',
        'title',
        'description',
      )


admin.site.register(Task, UnitAPIScheduleAdmin)