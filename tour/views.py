# tour/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Tour, TourBooking, TourReview
from .serializers import TourSerializer, TourBookingSerializer, TourReviewSerializer
from django.shortcuts import get_object_or_404

# ایجاد تور
class CreateTour(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        data['leader'] = request.user.id  # لیدر تور باید کاربر باشد
        serializer = TourSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# مشاهده لیست تورها
class TourList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tours = Tour.objects.all()
        serializer = TourSerializer(tours, many=True)
        return Response(serializer.data)

# مشاهده جزئیات یک تور خاص
class TourDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        tour = get_object_or_404(Tour, pk=pk)
        serializer = TourSerializer(tour)
        return Response(serializer.data)

# ثبت‌نام در یک تور
class RegisterForTour(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, tour_id):
        tour = get_object_or_404(Tour, pk=tour_id)
        user = request.user

        # بررسی اینکه آیا کاربر قبلاً در این تور ثبت‌نام کرده است یا خیر
        if TourBooking.objects.filter(tour=tour, user=user).exists():
            return Response({"message": "User already registered for this tour."}, status=status.HTTP_400_BAD_REQUEST)

        # ثبت‌نام کاربر در تور
        booking = TourBooking(tour=tour, user=user, payment_status="Pending", status="Registered")
        booking.save()
        return Response({"message": "User successfully registered for the tour."}, status=status.HTTP_201_CREATED)

# مشاهده نظرات و امتیازهای یک تور
class TourReviews(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, tour_id):
        tour = get_object_or_404(Tour, pk=tour_id)
        reviews = TourReview.objects.filter(tour=tour)
        serializer = TourReviewSerializer(reviews, many=True)
        return Response(serializer.data)

# ارسال نظر و امتیاز برای یک تور
class CreateTourReview(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, tour_id):
        tour = get_object_or_404(Tour, pk=tour_id)
        data = request.data
        data['user'] = request.user.id  # کاربر باید در نظر ذکر شود
        data['tour'] = tour_id  # تور باید ذکر شود

        serializer = TourReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
