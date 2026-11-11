from django.contrib import admin

from clinics.models import Specialty, Clinic, Service, WeeklyScedule, SceduleException, Appointment, NotificationLog




admin.site.register(Specialty)
admin.site.register(Clinic)
admin.site.register(SceduleException)
admin.site.register(Appointment)
admin.site.register(NotificationLog)









@admin.register(WeeklyScedule)
class WeeklySceduleAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'weekday', 'start_time', 'end_time')
    
    # Автоматические фильтры по полям
    list_filter = ('doctor', 'weekday')
    
    
    

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "clinic", "price")