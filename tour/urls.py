# tour/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # مسیر برای ایجاد تور
    path('create/', views.CreateTour.as_view(), name='create_tour'),

    # مسیر برای مشاهده لیست تورها
    path('list/', views.TourList.as_view(), name='tour_list'),

    # مسیر برای مشاهده جزئیات یک تور خاص
    path('detail/<int:pk>/', views.TourDetail.as_view(), name='tour_detail'),

    # مسیر برای ثبت‌نام در یک تور
    path('register/<int:tour_id>/', views.RegisterForTour.as_view(), name='register_for_tour'),

    # مسیر برای دیدن نظرات و امتیازها
    path('reviews/<int:tour_id>/', views.TourReviews.as_view(), name='tour_reviews'),

    # مسیر برای امتیازدهی و ارسال نظر
    path('review/<int:tour_id>/', views.CreateTourReview.as_view(), name='create_tour_review'),
]

