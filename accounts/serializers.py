from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError







class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 8,
            }
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    
    
    


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = auth.authenticate(
            request=self.context.get("request"),
            email=email,
            password=password
        )

        if not user:
            raise AuthenticationFailed("Invalid email or password")

        if not user.is_active:
            raise AuthenticationFailed("Your account is disabled")

        refresh = RefreshToken.for_user(user)

        return {
            "email": user.email,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
        
        
        
        
        


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
            
            
    