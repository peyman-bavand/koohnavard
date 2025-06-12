# user/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login
from rest_framework import status
from .models import CustomUser, UserProfile, NotificationSettings
from .serializers import UserProfileSerializer, NotificationSettingsSerializer, CustomUserSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication



class UserSignUpView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else: 
            print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User logged in successfully",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)



class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            bio = request.data.get('bio')
            address = request.data.get('address')
           
            # بررسی کنید که آیا کاربر قبلاً پروفایل دارد یا خیر
            if UserProfile.objects.filter(user=request.user).exists():
                return Response({'error': 'کاربر قبلاً پروفایل دارد. برای به‌روزرسانی از endpoint دیگری استفاده کنید.'}, status=status.HTTP_409_CONFLICT)

            # ساخت یک پروفایل کاربری جدید
            user_profile = UserProfile(user=request.user, bio=bio, address=address)
            user_profile.save()

            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': f'خطای سرور در هنگام ساخت پروفایل: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
    

class UserProfileEditView(APIView):
    authentication_classes = [JWTAuthentication]
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
            notification_settings, created = NotificationSettings.objects.get_or_create(
                user=request.user,
                defaults={}
            )
            serializer = NotificationSettingsSerializer(notification_settings)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Error retrieving or creating notification settings: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        try:
            notification_settings, created = NotificationSettings.objects.get_or_create(user=request.user)
            serializer = NotificationSettingsSerializer(notification_settings, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Error updating notification settings: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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