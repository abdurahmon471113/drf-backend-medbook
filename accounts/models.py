from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

from phonenumber_field.modelfields import PhoneNumberField
from clinics.models import BaseModel, Specialty, Clinic
from .choices import AccountChoice

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "admin")


        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)

            


class User(AbstractUser):
    username = None
    
    email = models.EmailField("Email address", max_length=250, null=True, blank=True, unique=True)
    role = models.CharField(choices=AccountChoice, default=AccountChoice.PATIENT)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = UserManager()

    
    def __str__(self):
        return self.email
    
    
    
class PatientProfile(BaseModel):
    patient = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_profile")  
    phone_number = PhoneNumberField(max_length=20, unique=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"Patient: {self.user.email}"
    
    
class DoctorProfile(BaseModel):
    doctor = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
    clinic = models.ForeignKey(Clinic, on_delete=models.PROTECT)
    specialities = models.ManyToManyField(Specialty, related_name="doctor_profiles")
    bio = models.TextField(blank=True, default="")  
    is_active = models.BooleanField(default=True)  
    
    def __str__(self):
        return f"Doctor: {self.user.email}"
    
    

    
    

    
    
    
    
