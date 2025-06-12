# tour/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from group.models import Group
from .models import Tour, TourBooking, TourReview, TourCategory
from .serializers import TourDetailSerializer
from .serializers import TourSerializer, TourBookingSerializer, TourReviewSerializer, TourCategorySerializer
from django.shortcuts import get_object_or_404



# گرفتن کتگوری ها
class TourCategoryList(APIView):
    permission_classes = [AllowAny]  # اگر عمومی هست

    def get(self, request):
        categories = TourCategory.objects.all()
        serializer = TourCategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# ایجاد تور
# class CreateTour(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         data = request.data
#         data['leader'] = request.user.id  # لیدر تور باید کاربر باشد
#         serializer = TourSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CreateTour(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        try:
            group = Group.objects.get(leader=user)
        except Group.DoesNotExist:
            return Response({'detail': 'گروه مربوط به این کاربر یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        # data['leader'] = user.id
        # data['group'] = group.id

        serializer = TourSerializer(data=data)
        if serializer.is_valid():
            serializer.save(leader=user, group=group)
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
# views.py


class TourDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        tour = get_object_or_404(Tour, pk=pk)
        serializer = TourDetailSerializer(tour)
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



# views.py

class TourReviewEligibility(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        tour = get_object_or_404(Tour, pk=pk)

        # بررسی ثبت‌نام کاربر در تور
        is_registered = TourBooking.objects.filter(tour=tour, user=user).exists()

        # بررسی اینکه آیا کاربر قبلاً نظر داده
        has_reviewed = TourReview.objects.filter(tour=tour, user=user).exists()

        return Response({
            "is_registered": is_registered,
            "has_reviewed": has_reviewed
        })



class SubmitTourReview(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data.copy()

        # بررسی اینکه آیا تور وجود دارد
        try:
            tour_id = data.get("tour")
            tour = Tour.objects.get(id=tour_id)
        except Tour.DoesNotExist:
            return Response({"detail": "تور پیدا نشد."}, status=status.HTTP_404_NOT_FOUND)

        # بررسی اینکه کاربر قبلاً نظر نداده
        if TourReview.objects.filter(user=user, tour=tour).exists():
            return Response({"detail": "شما قبلاً برای این تور نظر داده‌اید."}, status=status.HTTP_400_BAD_REQUEST)

        # اضافه کردن کاربر به دیتا برای سریالایزر
        data["user"] = user.id

        serializer = TourReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
