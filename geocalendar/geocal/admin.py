from django.contrib import admin

from django.utils.translation import ugettext_lazy as _
from geocal.models import CalendarEntry

class CalendarAdmin(admin.ModelAdmin):
    model = CalendarEntry
    extra = 3


admin.site.register(CalendarEntry, CalendarAdmin)