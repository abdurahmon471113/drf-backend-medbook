from django.db import models



class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True
        
        
class Specialty(BaseModel):
    name = models.CharField(max_length=255)
        
    def __str__(self):
        return self.name    
    
    
    
        
        
class Clinic(BaseModel):
    name = models.CharField(max_length=50)
    address = models.TextField()

    def __str__(self):
        return self.name
    
    
    
    
class Service(BaseModel):
    clinic = models.ForeignKey(Clinic, on_delete=models.PROTECT)
    name = models.CharField(max_length=500)
    description = models.TextField(blank=True, default="")
    duration_minutes = models.PositiveIntegerField(default=30)
    buffer_minutes = models.PositiveIntegerField(default=10)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    is_active = models.BooleanField(default=True) 
    doctors = models.ManyToManyField("accounts.DoctorProfile", related_name="doctor_profiles")
    
    
    
    
class WeeklyScedule(BaseModel):
    DAYS_OF_THE_WEEKDAY = [
    ("MON", "Monday"),
    ("TUE", "Tuesday"),
    ("WED", "Wednesday"),
    ("THU", "Thursday"),
    ("FRI", "Friday"),
    ("SAT", "Saturday"),
    ("SUN", "Sunday"),
]
    
    doctor = models.ForeignKey("accounts.DoctorProfile", on_delete=models.CASCADE)
    weekday = models.CharField(max_length = 20, choices = DAYS_OF_THE_WEEKDAY, default = 'MON')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    
    
    
class SceduleException(BaseModel):
    TYPE_CHOICES = [
        ("unavailable", "Unavailable"),
        ("extra_hours", "Extra hours"),
    ]
     

    doctor = models.ForeignKey("accounts.DoctorProfile", on_delete=models.PROTECT, related_name="scedule_exception")
    start = models.TimeField()
    end = models.TimeField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    reason = models.TextField(blank=True, default="")



class Appointment(BaseModel):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
        ("no_show", "No show"),
        ("expired", "Expired"),
    ]
    
    patient = models.ForeignKey("accounts.PatientProfile", on_delete=models.PROTECT, related_name="appointments")
    doctor = models.ForeignKey("accounts.DoctorProfile", on_delete=models.PROTECT, related_name="appointments")
    clinic = models.ForeignKey(Clinic, on_delete=models.PROTECT, related_name="appointments")
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="appointments")
    start = models.DateTimeField()
    end = models.DateTimeField()
    status = models.CharField(max_length=20, default="pending")
    price = models.DecimalField(max_digits=12, decimal_places=0)
    currency = models.CharField(max_length=3, default="UZS")
    patient_note = models.TextField(blank=True, default="")
    cancel_reason = models.TextField(blank=True, default="")
    reschedule_count = models.PositiveSmallIntegerField(default=0)
    
    
    
 
class NotificationLog(BaseModel):
    TYPE_CHOICES = [
    ("appointment_reminder", "Appointment reminder"),
    ("appointment_confirmed", "Appointment confirmed"),
    ("appointment_cancelled", "Appointment cancelled"),
    ("appointment_rescheduled", "Appointment rescheduled"),
]
    CHANNEL_CHOICES = [
    ("email", "Email"),
    ("sms", "SMS"),
    ("push", "Push notification"),
] 
    STATUS_CHOICES = [
    ("pending", "Pending"),
    ("sent", "Sent"),
    ("failed", "Failed"),
]
    
    appointment = models.ForeignKey(Appointment, on_delete=models.PROTECT, related_name="notification_logs")
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    sent_at = models.DateTimeField(blank=True, null=True)
    
    
    

    


    

     
