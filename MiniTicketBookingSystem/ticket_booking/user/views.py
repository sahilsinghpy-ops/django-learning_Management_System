from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer

# ====================== REGISTER VIEW ======================
class RegisterView(generics.CreateAPIView):
    """
    User Registration API
    Anyone can register (no login required)
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]   # Koi bhi register kar sakta hai

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "message": "User registered successfully!",
            "username": user.username,
            "user_type": user.user_type
        }, status=status.HTTP_201_CREATED)