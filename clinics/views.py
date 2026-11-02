from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class TestGetView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message": "You are authenticated!",
            "user": request.user.email
        })
        
        