from rest_framework import serializers
from accounts.models import PatientProfile, DoctorProfile, Clinic, Specialty







class PatientProfileSerializator(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = "__all__"
        
        
        
class SpecialtySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Specialty
        fields = ["name"]


class ClinicSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Clinic
        exclude = ["id", "updated_at", "created_at"]
        
        
class DoctorProfileSerializator(serializers.ModelSerializer):
    clinic = ClinicSerializer()
    specialities = SpecialtySerializer(many=True)
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["full_name"] = f"{instance.user.first_name} {instance.user.last_name}"
        return ret
    
    class Meta:
        model = DoctorProfile
        exclude = ["updated_at", "created_at", "is_active"]
        
        
    
    
    
    
    
