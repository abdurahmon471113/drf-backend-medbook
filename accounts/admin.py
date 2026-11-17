from django.contrib import admin

from accounts.models import DoctorProfile, PatientProfile, User

admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email"]

    # Автоматические фильтры по полям
    # list_filter = (["email"])
