from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserLoginSerializer, UserRegisterSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class Home(APIView):
    def get(self, request):
        return Response ({"message": "Nextjs and Django auth_application api work correctly!"})
    

# user registration functionality
class UserRegister(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = User(
                username = serializer.validated_data['username'],
                email = serializer.validated_data['email']
            )
            user.set_password(serializer.validated_data['password'])
            user.save()
            response_serializer = UserRegisterSerializer(user)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# user login functionality
def authenticate_with_email(email, password):
    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            return user
    except User.DoesNotExist:
        return None
class UserLogin(APIView):
    def post(self, request):
        #username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({"detail": "Username and Password are required!"})
        user = authenticate_with_email(email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            serializer = UserLoginSerializer(user)
            return Response({
                "id": user.id,
                "user": serializer.data,
                "username": user.username,
                "email": user.email,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid credentials!"}, status=status.HTTP_401_UNAUTHORIZED)