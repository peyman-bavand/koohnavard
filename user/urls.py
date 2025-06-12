from django.urls import path
from .views import UserSignUpView, UserLoginView, UserProfileView, UserProfileEditView, NotificationSettingsView, NotificationSettingsEditView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
) 


urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='user_signup'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/edit/', UserProfileEditView.as_view(), name='user_profile_edit'),
    path('notifications/', NotificationSettingsView.as_view(), name='notification_settings'),
    path('notifications/edit/', NotificationSettingsEditView.as_view(), name='notification_settings_edit'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
 

#signup: این مسیر به صفحه ثبت‌نام کاربر هدایت می‌کند.
#login: این مسیر به صفحه ورود کاربر هدایت می‌کند.
#profile: این مسیر برای نمایش پروفایل کاربر استفاده می‌شود.
#profile/edit: این مسیر برای ویرایش پروفایل کاربر استفاده می‌شود.
#notifications: این مسیر به صفحه تنظیمات نوتیفیکیشن‌های کاربر هدایت می‌کند.
#notifications/edit: این مسیر برای ویرایش تنظیمات نوتیفیکیشن‌ها است.