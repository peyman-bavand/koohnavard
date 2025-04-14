# tour/serializers.py

from rest_framework import serializers
from .models import Tour, TourBooking, TourReview
from django.contrib.auth import get_user_model
from group.models import Group
from .models import TourCategory
from rest_framework import serializers
# Serializer برای مدل تور



class TourSerializer(serializers.ModelSerializer):
    leader = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=TourCategory.objects.all())

    class Meta:
        model = Tour
        fields = ['id', 'title', 'description', 'leader', 'start_date', 'end_date', 'price', 'category', 'location', 'group']

# Serializer برای مدل ثبت‌نام در تور
class TourBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourBooking
        fields = ['id', 'user', 'tour', 'booked_at']
        read_only_fields = ['user', 'booked_at']   

        
# Serializer برای مدل نظرات و امتیازها
class TourReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    tour = serializers.PrimaryKeyRelatedField(queryset=Tour.objects.all())

    class Meta:
        model = TourReview
        fields = ['id', 'tour', 'user', 'rating', 'comment', 'created_at']


# tour/serializers.py




