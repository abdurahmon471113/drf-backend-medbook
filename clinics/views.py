from rest_framework.views import APIView
from rest_framework import generics, status, views, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from accounts.models import PatientProfile, DoctorProfile
from .serializers import PatientProfileSerializator, DoctorProfileSerializator
from django_filters.rest_framework import DjangoFilterBackend






class FindDoctorAPI(generics.ListAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializator
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = []
