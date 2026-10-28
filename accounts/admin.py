from django.contrib import admin

from accounts.models import User, PatientProfile, DoctorProfile



admin.site.register(User)
admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)


