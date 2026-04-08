from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from .serializers import RegisterSerializer, UserSerializer, LoginSerialization
from django.shortcuts import render


def register_page(request):
    return render(request,'users/register.html')


def login_page(request):
    return render(request, 'users/login.html')

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def get(self, request, *args, **kwargs):
        return Response({"message": "Send a POST request to register."})

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully",
                "user": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CookieLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerialization

    def get(self, request, *args, **kwargs):
        return Response({"message": "Please enter your credentials."})

    def post(self, request, *args, **kwargs):
        serializer = LoginSerialization(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response = Response({
                "message": "Login successful",
                "role": user.role,
                "username": user.username
            }, status=status.HTTP_200_OK)

            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                samesite='Lax',
                secure=False,
            )
            return response

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        response = Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        return response