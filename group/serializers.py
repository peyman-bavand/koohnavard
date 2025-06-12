# group/serializers.py

from rest_framework import serializers
from .models import Group, GroupMember, GroupImageGallery, GroupImageGallery
from django.contrib.auth import get_user_model

# Serializer برای مدل گروه
class GroupSerializer(serializers.ModelSerializer):
    leader = serializers.ReadOnlyField(source='leader.id')

    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'leader', 'created_at', 'updated_at']

# Serializer برای مدل اعضای گروه
class GroupMemberSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())

    class Meta:
        model = GroupMember
        fields = ['id', 'user', 'group', 'joined_at', 'status', 'role']

# Serializer برای مدل گالری تصاویر گروه


class GroupImageGallerySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    group = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = GroupImageGallery
        fields = ['id', 'group', 'image', 'image_url', 'caption', 'uploaded_at']
        read_only_fields = ['uploaded_at']

    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            request = self.context.get('request')
            url = obj.image.url
            return request.build_absolute_uri(url) if request else url
        return None
