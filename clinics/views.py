from rest_framework.views import APIView
from rest_framework import generics, status, views, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from accounts.models import PatientProfile, DoctorProfile
from clinics.models import Service, WeeklyScedule, Clinic
from .serializers import PatientProfileSerializator, DoctorProfileSerializator, ServiceSerializer, AvailableDateSerializer
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from datetime import date, timedelta









# This view is for patients for finding only active doctors by filters page
class FindDoctorAPI(generics.ListAPIView):
    queryset = DoctorProfile.objects.filter(is_active=True)
    serializer_class = DoctorProfileSerializator
    permission_classes = [AllowAny]

    


    def get_queryset(self):
        queryset = super().get_queryset()
        
        # search by first name filter
        if search := self.request.GET.get("search"):
            for i in search.split():
                queryset = queryset.filter(Q(user__first_name__icontains=i) | Q(user__last_name__icontains=i))

        # city filter
        if city := self.request.GET.get("city"):
            queryset = queryset.filter(clinic__city__iexact=city)
            
        # specialy filter 
        if specialty := self.request.GET.get("specialty"):
            queryset = queryset.filter(specialities__name__iexact=specialty)
        
        # minimum price filter
        if price_min := self.request.GET.get("price_min"):
            queryset = queryset.filter(doctor_profile__price__gte=price_min)
            
        # maximum price filter    
        if price_max := self.request.GET.get("price_max"):
            queryset = queryset.filter(doctor_profile__price__lte=price_max)
            
        # ordering prices filter
        if ordering := self.request.GET.get("ordering"):
            if ordering == "price":
                # Cheapest doctors first
                queryset = queryset.order_by("price")

            elif ordering == "-price":
                # Costliest doctors first
                queryset = queryset.order_by("-price")
        return queryset


class DoctorServiceDetailAPI(APIView):
    permission_classes = [AllowAny]  # For a momentum, then decode with permissions

    def get(self, request, pk):
        doctor = get_object_or_404(DoctorProfile, pk=pk, is_active=True)
        services = Service.objects.filter(is_active=True, doctors=doctor)
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)

        
        


class AvailableSlotsAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        print("AVAILABLE SLOTS VIEW STARTED", flush=True)

        doctor = get_object_or_404(
            DoctorProfile,
            pk=pk,
            is_active=True
        )
        
        print(doctor.user.first_name[1:])

        # 1. Get dates from query parameters
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")

        if not date_from or not date_to:
            raise ValidationError("Both dates are required.")

        # 2. Convert strings into date objects
        try:
            date_from = date.fromisoformat(date_from)
            date_to = date.fromisoformat(date_to)
        except ValueError:
            raise ValidationError("Use YYYY-MM-DD format.")

        # 3. Validate date range
        if date_from > date_to:
            raise ValidationError("Invalid date range.")

        max_date = date_from + timedelta(days=14)

        if date_to > max_date:
            raise ValidationError(
                "You can select a maximum of 14 days."
            )

        results = []

        # 4. Check every selected date
        current_date = date_from

        while current_date <= date_to:

            weekday = current_date.strftime("%a").upper()

            print(
                f"DATE: {current_date} | WEEKDAY: {weekday}",
                flush=True
            )

            weekly_schedule = WeeklyScedule.objects.filter(
                weekday=weekday,
                doctor=doctor
            )

            # 5. Check doctor's working schedule
            if weekly_schedule.exists():
                status = "Free"
            else:
                status = "Day off"

            results.append({
                "date": current_date,
                "weekday": weekday,
                "count": weekly_schedule.count(),
                "status": status,
                "slots": weekly_schedule,
                "clinic_timezone": doctor.clinic.timezone
            })

            current_date += timedelta(days=1)

        # 6. Serialize results
        serializer = AvailableDateSerializer(
            results,
            many=True,
            context={"doctor": doctor}
        )

        return Response({
            "results": serializer.data
        })

    
    
    
 

