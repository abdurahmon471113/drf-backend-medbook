from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer, PatientProfileSerializator, DoctorProfileSerializator
from .models import PatientProfile, DoctorProfile







class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    
    
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK
        )
    
    
    
class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Logout successful"},
            status=status.HTTP_200_OK
        )
        
        
        
class FindDoctor(generics.ListAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializator
    permission_classes = [AllowAny]
