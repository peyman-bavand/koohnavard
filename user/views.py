# user/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from rest_framework import status
from .models import CustomUser, UserProfile, NotificationSettings
from .serializers import UserProfileSerializer, NotificationSettingsSerializer, CustomUserSerializer


class UserSignupView(APIView):
    def post(self, request):
        form = UserCreationForm(request.data)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Login the user after successful registration
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "User logged in successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)


class UserProfileEditView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User profile updated successfully"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)


class NotificationSettingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            notification_settings = NotificationSettings.objects.get(user=request.user)
            serializer = NotificationSettingsSerializer(notification_settings)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NotificationSettings.DoesNotExist:
            return Response({"error": "Notification settings not found"}, status=status.HTTP_404_NOT_FOUND)


class NotificationSettingsEditView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            notification_settings = NotificationSettings.objects.get(user=request.user)
            serializer = NotificationSettingsSerializer(notification_settings, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Notification settings updated successfully"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except NotificationSettings.DoesNotExist:
            return Response({"error": "Notification settings not found"}, status=status.HTTP_404_NOT_FOUND)

# Create your views here.
#UserSignupView: API برای ثبت‌نام کاربر است که پس از موفقیت‌آمیز بودن درخواست، کاربر را وارد سیستم می‌کند.
#UserLoginView: API برای ورود کاربر است. این API چک می‌کند که آیا اعتبار کاربر صحیح است یا خیر.
#UserProfileView: API برای دریافت پروفایل کاربر است.
#UserProfileEditView: API برای ویرایش پروفایل کاربر است.
#NotificationSettingsView: API برای دریافت تنظیمات نوتیفیکیشن کاربر است.
#NotificationSettingsEditView: API برای ویرایش تنظیمات نوتیفیکیشن کاربر است.