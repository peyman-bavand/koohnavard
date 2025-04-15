# tour/factories.py

import factory
from factory.django import DjangoModelFactory
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

from group.factories import GroupFactory  # فرض بر اینکه GroupFactory رو ساختی
from tour.models import TourCategory, Tour, TourBooking, TourReview

User = get_user_model()

class TourCategoryFactory(DjangoModelFactory):
    class Meta:
        model = TourCategory

    name = factory.Faker('word')
    description = factory.Faker('text')


class TourFactory(DjangoModelFactory):
    class Meta:
        model = Tour

    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('paragraph')
    leader = factory.SubFactory('user.factories.UserFactory')  # اگه UserFactory جای دیگه ساختی
    start_date = factory.LazyFunction(lambda: timezone.now().date())
    end_date = factory.LazyFunction(lambda: (timezone.now() + timedelta(days=5)).date())
    price = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    category = factory.SubFactory(TourCategoryFactory)
    location = factory.Faker('city')
    group = factory.SubFactory(GroupFactory)


class TourBookingFactory(DjangoModelFactory):
    class Meta:
        model = TourBooking

    user = factory.SubFactory('user.factories.UserFactory')
    tour = factory.SubFactory(TourFactory)
    booking_date = factory.LazyFunction(timezone.now)


class TourReviewFactory(DjangoModelFactory):
    class Meta:
        model = TourReview

    tour = factory.SubFactory(TourFactory)
    user = factory.SubFactory('user.factories.UserFactory')
    rating = factory.Iterator([1, 2, 3, 4, 5])
    comment = factory.Faker('paragraph')
    created_at = factory.LazyFunction(timezone.now)
