from django.contrib import admin
from .models import TourBooking, TourReview, Tour, TourCategory
# Register your models here.

admin.site.register(TourBooking)
admin.site.register(TourReview)
admin.site.register(Tour)
admin.site.register(TourCategory)
