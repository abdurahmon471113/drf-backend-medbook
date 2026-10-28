from django.db.models import TextChoices


class AccountChoice(TextChoices):
    PATIENT = ("PAT", "Patient")
    DOCTOR = ("DOC", "Doctor")
