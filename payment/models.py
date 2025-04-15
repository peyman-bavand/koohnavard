# payment/models.py

from django.db import models
from django.conf import settings
from tour.models import Tour

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    authority = models.CharField(max_length=100, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.total_amount} - {'پرداخت شده' if self.is_paid else 'پرداخت نشده'}"

class PaymentItem(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
 