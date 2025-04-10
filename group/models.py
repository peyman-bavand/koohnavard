from django.db import models
from django.conf import settings

class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
       return self.name

class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Member', 'Member'), ('Leader', 'Leader'), ('Left', 'Left')])
    role = models.CharField(max_length=50, choices=[('Member', 'Member'), ('Leader', 'Leader'), ('Manager', 'Manager')])
    
    def __str__(self):
        return f"{self.user.username} - {self.group.name}"
    

class GroupImageGallery(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='group_images/')
    caption = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.group.name}"