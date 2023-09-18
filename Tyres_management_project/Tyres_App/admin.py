from django.contrib import admin
from .models import Car, TyreSet, RaceWeekend, WeekendSession , WeekendFormat,WeekendTemplate

admin.site.register(Car)
admin.site.register(TyreSet)
admin.site.register(RaceWeekend)
admin.site.register(WeekendSession)
admin.site.register(WeekendTemplate)

admin.site.register(WeekendFormat)
