from django.contrib import admin
from .models import CustomUser, UserProfile, NotificationSettings


admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(NotificationSettings)
