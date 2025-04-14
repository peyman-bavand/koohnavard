from django.contrib import admin
from .models import Payment, PaymentItem


# Register your models here.
admin.site.register(Payment)
admin.site.register(PaymentItem)
