# payment/urls.py

from django.urls import path
from .views import CreatePaymentView, VerifyPaymentView, PaymentListView, UserPaymentAndTourBookingView

urlpatterns = [
    path('create/', CreatePaymentView.as_view(), name='payment-create'),
    path('verify/<int:payment_id>/', VerifyPaymentView.as_view(), name='payment-verify'),
    path('my-payments/', PaymentListView.as_view(), name='my-payments'),
    path('user/payments-and-bookings/', UserPaymentAndTourBookingView.as_view(), name='user-payments-and-bookings'),
    # payment/urls.py
]
