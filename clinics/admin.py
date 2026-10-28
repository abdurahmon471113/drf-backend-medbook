from django.contrib import admin

from clinics.models import Specialty, Clinic, Service, WeeklyScedule, SceduleException, Appointment, NotificationLog




admin.site.register(Specialty)
admin.site.register(Clinic)
admin.site.register(Service)
admin.site.register(WeeklyScedule)
admin.site.register(SceduleException)
admin.site.register(Appointment)
admin.site.register(NotificationLog)