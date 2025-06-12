# tour/serializers.py

from rest_framework import serializers
from .models import Tour, TourBooking, TourReview, TourCategory
from django.contrib.auth import get_user_model
from group.models import Group
from rest_framework import serializers
# Serializer برای مدل تور



class TourCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TourCategory
        fields = ['id', 'name', 'description']


class TourSerializer(serializers.ModelSerializer):
    leader = serializers.PrimaryKeyRelatedField(read_only=True)
    group = serializers.PrimaryKeyRelatedField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=TourCategory.objects.all())

    class Meta:
        model = Tour
        fields = [
            'id', 'title', 'description', 'leader',
            'start_date', 'end_date', 'price',
            'category', 'location', 'group'
        ]



   
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




######################################این مجموعه سریالایزر برای استفاده در کامپوننت tour detail ساخته شدند
# serializers.py

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class TourDetailSerializer(serializers.ModelSerializer):
    leader = SimpleUserSerializer(read_only=True)
    group = GroupSerializer(read_only=True)
    category = TourCategorySerializer(read_only=True)

    class Meta:
        model = Tour
        fields = [
            'id', 'title', 'description', 'leader',
            'start_date', 'end_date', 'price',
            'category', 'location', 'group'
        ]


