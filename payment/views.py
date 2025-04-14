# payment/views.py

import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Payment, PaymentItem
from .serializers import PaymentSerializer
from tour.models import Tour, TourBooking  
from notification.models import Notification
from rest_framework import status
from payment.models import Payment
from payment.serializers import PaymentSerializer
from tour.serializers import TourBookingSerializer
from rest_framework.generics import ListAPIView

    # payment/views.py



ZARINPAL_MERCHANT_ID = settings.ZARINPAL_MERCHANT_ID
ZARINPAL_REQUEST_URL = 'https://api.zarinpal.com/pg/v4/payment/request.json'
ZARINPAL_VERIFY_URL = 'https://api.zarinpal.com/pg/v4/payment/verify.json'
ZARINPAL_START_PAY_URL = 'https://www.zarinpal.com/pg/StartPay/'

class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tour_id = request.data.get('tour_id')
        amount = request.data.get('amount')

        try:
            tour = Tour.objects.get(id=tour_id)
        except Tour.DoesNotExist:
            return Response({'error': 'تور یافت نشد'}, status=404)

        payment = Payment.objects.create(
            user=request.user,
            total_amount=amount,
            is_paid=False
        )

        PaymentItem.objects.create(payment=payment, tour=tour, amount=amount)

        callback_url = f"https://your-domain.com/payment/verify/{payment.id}/"
        data = {
            "merchant_id": ZARINPAL_MERCHANT_ID,
            "amount": int(float(amount) * 10),
            "callback_url": callback_url,
            "description": f"پرداخت برای تور: {tour.title}",
        }

        headers = {'accept': 'application/json', 'content-type': 'application/json'}
        response = requests.post(ZARINPAL_REQUEST_URL, json=data, headers=headers)
        result = response.json()

        if result.get('data') and result['data'].get('authority'):
            authority = result['data']['authority']
            payment.authority = authority
            payment.save()
            payment_url = ZARINPAL_START_PAY_URL + authority
            return Response({'payment_url': payment_url})
        return Response({'error': 'مشکلی در ایجاد پرداخت وجود دارد'}, status=400)



class VerifyPaymentView(APIView):
    def get(self, request, payment_id):
        try:
            payment = Payment.objects.get(id=payment_id, is_paid=False)
        except Payment.DoesNotExist:
            return Response({'error': 'پرداخت یافت نشد'}, status=404)

        authority = request.GET.get('Authority')
        status_param = request.GET.get('Status')

        if status_param != 'OK':
            return Response({'error': 'پرداخت توسط کاربر لغو شد'}, status=400)

        data = {
            "merchant_id": ZARINPAL_MERCHANT_ID,
            "amount": int(float(payment.total_amount) * 10),
            "authority": authority
        }

        headers = {'accept': 'application/json', 'content-type': 'application/json'}
        response = requests.post(ZARINPAL_VERIFY_URL, json=data, headers=headers)
        result = response.json()

        if result.get('data') and result['data'].get('code') == 100:
            # پرداخت موفق
            payment.is_paid = True
            payment.save()

            # ثبت‌نام کاربر در تور
            payment_item = payment.paymentitem_set.first()  # فرض بر این است که یک تور در payment_item وجود دارد
            tour = payment_item.tour

            # ثبت‌نام کاربر در تور
            TourBooking.objects.create(user=payment.user, tour=tour)

            # ایجاد نوتیفیکیشن
            Notification.objects.create(
                user=payment.user,
                title='پرداخت موفق',
                message=f'پرداخت شما برای تور "{tour.title}" با موفقیت انجام شد و شما به این تور ثبت‌نام شدید.',
            )

            return Response({'status': 'پرداخت موفق', 'ref_id': result['data']['ref_id']})
        return Response({'error': 'تأیید پرداخت ناموفق'}, status=400)
    



class UserPaymentAndTourBookingView(APIView):
    def get(self, request):
        user = request.user  # کاربر فعلی که درخواست داده است
        
        # دریافت پرداخت‌های موفق کاربر
        payments = Payment.objects.filter(user=user, status='Success')
        payments_serializer = PaymentSerializer(payments, many=True)

        # دریافت ثبت‌نام‌های تورهای موفق کاربر
        tour_bookings = TourBooking.objects.filter(user=user)
        tour_bookings_serializer = TourBookingSerializer(tour_bookings, many=True)

        return Response({
            'payments': payments_serializer.data,
            'tour_bookings': tour_bookings_serializer.data
        })




class PaymentListView(ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).order_by('-created_at')