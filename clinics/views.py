from rest_framework.views import APIView
from rest_framework import generics, status, views, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from accounts.models import PatientProfile, DoctorProfile
from .serializers import PatientProfileSerializator, DoctorProfileSerializator
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q






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
    
    
    

