from rest_framework import serializers
from accounts.models import PatientProfile, DoctorProfile, Clinic, Specialty
from clinics.models import Service, WeeklyScedule







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
        
        

class DoctorNameSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = DoctorProfile
        fields = ["id", "full_name"]

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    
    
        
        
class DoctorProfileSerializator(serializers.ModelSerializer):
    clinic = ClinicSerializer()
    specialities = SpecialtySerializer(many=True)

    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["full_name"] = instance.user.get_full_name()
        return ret
    
    class Meta:
        model = DoctorProfile
        exclude = ["updated_at", "created_at", "is_active"]
        
        
        
        
    
    
    
class ServiceSerializer(serializers.ModelSerializer):
    doctor = DoctorProfileSerializator(many=True, read_only=True)
    doctors = DoctorNameSerializer(many=True, read_only=True)


    
    class Meta:
        model = Service
        exclude = ["is_active"]
        
        
        
        
    # def get_full_name(self, obj):
    #     return f"{obj.user.first_name} {obj.user.last_name}"
    
    
    
class WeeklySceduleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WeeklyScedule
        fields = ["start_time", "end_time"]
    
    
    



class AvailableDateSerializer(serializers.Serializer):
    
    slots = WeeklySceduleSerializer(many=True, read_only=True)
    doctor = serializers.SerializerMethodField()
    date = serializers.DateField()
    weekday = serializers.CharField()
    status = serializers.CharField()
    clinic_timezone  = serializers.CharField()
    count = serializers.IntegerField()
    
    def get_doctor(self, obj):
        doctor = self.context["doctor"]

        return {
            "id": doctor.id,
            "full_name": doctor.user.get_full_name()
        }
    
    

    
    
