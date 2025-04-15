from django.db import models
from django.conf import settings
from group.models import Group



class TourCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    

class Tour(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(TourCategory, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class TourBooking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.tour.title}"



class TourReview(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

 